import sys
from typing import Mapping, Optional, Sequence

from sidewinder.compiler_toolchain.ast import (
    BinaryExprAST,
    CallExprAST,
    ExprAST,
    FunctionAST,
    NumberExprAST,
    PrototypeAST,
    VariableExprAST,
)
from sidewinder.compiler_toolchain.lexer import Lexer
from sidewinder.compiler_toolchain.token import Token

_binary_op_precedence_map: Mapping[str, int] = {
    "<": 10,
    ">": 10,
    "+": 20,
    "-": 20,
    "*": 40,
    "/": 40,
}


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer: Lexer = lexer
        self._current_token: Optional[Token] = None

    def parse(self) -> None:
        # Prime first token
        print("ready> ", file=sys.stderr)
        self.get_next_token()

        while self._current_token is not None:
            token_type: Token.Type = self._current_token.token_type()
            token_value: Optional[str] = self._current_token.value()

            if token_type == Token.Type.EOF:
                return
            elif token_value == ";":  # TODO: temporarily ignore top-level semicolons
                self.get_next_token()
            elif token_type == Token.Type.DEF:
                self.handle_definition()
            elif token_type == Token.Type.EXTERN:
                self.handle_extern()
            else:
                self.handle_top_level_expression()

            print("ready> ", file=sys.stderr)

    def handle_definition(self) -> None:
        expr: Optional[ExprAST] = self.parse_definition()

        if expr:
            print("Parsed a function definition:", file=sys.stderr)
            print(f"output> {expr}", file=sys.stderr)

        # Skip token for error recovery
        self.get_next_token()

    def handle_extern(self) -> None:
        expr: Optional[ExprAST] = self.parse_extern()

        if expr:
            print("Parsed an extern:", file=sys.stderr)
            print(f"output> {expr}", file=sys.stderr)

        # Skip token for error recovery
        self.get_next_token()

    def handle_top_level_expression(self) -> None:
        expr: Optional[ExprAST] = self.parse_top_level_expression()

        if expr:
            print("Parsed a top-level expression:", file=sys.stderr)
            print(f"output> {expr}", file=sys.stderr)

        # Skip token for error recovery
        self.get_next_token()

    def empty_expression(self, reason: str) -> None:
        print(reason, file=sys.stderr)
        return None

    def get_next_token(self) -> None:
        self._current_token = self._lexer.try_get_next_token()

        print(f"next> {self._current_token}")

    # number
    def parse_number_expression(self) -> ExprAST:
        assert self._current_token
        assert self._current_token.value()

        expr = NumberExprAST(value=float(self._current_token.value()))

        # Consume number and move to next token
        self.get_next_token()

        return expr

    # '(' expression ')'
    def parse_parentheses_expression(self) -> Optional[ExprAST]:
        self.get_next_token()  # eat (

        v: Optional[ExprAST] = self.parse_expression()

        if not v:
            return None

        if self._current_token.value() != ")":
            return self.empty_expression(reason="expected ')'")

        self.get_next_token()  # eat )

        return v

    def parse_identifier_expression(self) -> Optional[ExprAST]:
        assert self._current_token
        assert self._current_token.value()

        identifier: str = self._current_token.value()

        self.get_next_token()

        # Simple variable
        if self._current_token.value() != "(":
            return VariableExprAST(name=identifier)

        # Function call
        self.get_next_token()

        args: Sequence[ExprAST] = []
        if self._current_token.value() != ")":
            while True:
                arg: Optional[ExprAST] = self.parse_expression()

                if not arg:
                    return self.empty_expression(reason="")

                args.append(arg)

                if self._current_token.value() == ")":
                    break

                if self._current_token.value() != ",":
                    return self.empty_expression(reason="Expected ')' or ',' in argument list")

                self.get_next_token()  # eat ,

            self.get_next_token()  # eat )

        return CallExprAST(callee=identifier, args=args)

    def parse_primary(self) -> Optional[ExprAST]:
        if not self._current_token:
            return None

        token_type: Token.Type = self._current_token.token_type()

        if token_type == Token.Type.IDENTIFIER:
            return self.parse_identifier_expression()
        elif token_type == Token.Type.NUMBER:
            return self.parse_number_expression()

        if self._current_token.value() == "(":
            return self.parse_parentheses_expression()

        return self.empty_expression(reason="unknown token when expecting an expression")

    def parse_expression(self) -> Optional[ExprAST]:
        lhs: Optional[ExprAST] = self.parse_primary()

        if not lhs:
            return None

        return self.parse_binary_op_rhs(expression_precedence=0, lhs=lhs)

    def parse_binary_op_rhs(self, expression_precedence: int, lhs: ExprAST) -> Optional[ExprAST]:
        while True:
            token_precedence: int = self.get_token_precedence(token=self._current_token)

            # If operator does not bind as tightly as the current one, we are done
            if token_precedence < expression_precedence:
                return lhs

            # This is a binop
            binary_op_token: Token = self._current_token
            self.get_next_token()  # eat the current token

            # Parse expression after binary operator
            rhs: Optional[ExprAST] = self.parse_primary()

            if not rhs:
                return None

            next_precedence: int = self.get_token_precedence(token=self._current_token)

            if token_precedence < next_precedence:
                rhs = self.parse_binary_op_rhs(token_precedence + 1, rhs)

                if not rhs:
                    return None

            # Merge LHS/RHS
            lhs = BinaryExprAST(op=binary_op_token.value(), lhs=lhs, rhs=rhs)

    def get_token_precedence(self, token: Optional[Token]) -> int:
        # -1 is the lowest precedence (or lack thereof)
        if not token:
            return -1

        return _binary_op_precedence_map.get(token.value(), -1)

    # id '(' id* ')'
    def parse_prototype(self) -> Optional[PrototypeAST]:
        if self._current_token.token_type() != Token.Type.IDENTIFIER:
            return self.empty_expression(
                reason=f"Expected function name in prototype, but got token of "
                f"type {self._current_token.token_type().name} with value "
                f"'{self._current_token.value()}'"
            )

        fn_name: str = self._current_token.value()

        self.get_next_token()

        if self._current_token.value() != "(":
            return self.empty_expression(
                reason=f"Expected '(' in prototype, but got '{self._current_token.value()}'"
            )

        arg_names: Sequence[str] = []

        self.get_next_token()  # consume '('

        while self._current_token.token_type() == Token.Type.IDENTIFIER:
            arg_names.append(self._current_token.value())
            self.get_next_token()  # consume arg

            # TODO: add comma-delimiter

        if self._current_token.value() != ")":
            return self.empty_expression(
                reason=f"Expected ')' in prototype, but got '{self._current_token.value()}'"
            )

        self.get_next_token()  # eat ')'

        return PrototypeAST(name=fn_name, args=arg_names)

    def parse_definition(self) -> Optional[FunctionAST]:
        self.get_next_token()  # consume def

        proto: Optional[PrototypeAST] = self.parse_prototype()

        if not proto:
            return None

        body: Optional[ExprAST] = self.parse_expression()

        if not body:
            return None

        return FunctionAST(proto=proto, body=body)

    def parse_top_level_expression(self) -> Optional[FunctionAST]:
        expr: Optional[ExprAST] = self.parse_expression()

        if not expr:
            return None

        # Make an anonymous proto
        proto = PrototypeAST(name="__anon_expr", args=[])
        return FunctionAST(proto=proto, body=expr)

    def parse_extern(self) -> Optional[PrototypeAST]:
        self.get_next_token()  # consume extern
        return self.parse_prototype()
