import sys
from typing import Optional, Sequence

from sidewinder.compiler_toolchain.lexer import Lexer
from sidewinder.compiler_toolchain.token import Token
from sidewinder.compiler_toolchain.ast import (
    CallExprAst,
    ExprAst,
    NumberExprAst,
    VariableExprAst,
)


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer: Lexer = lexer
        self._current_token: Optional[Token] = None

    def parse(self) -> None:
        pass

    def empty_expression(reason: str) -> None:
        print(reason, file=sys.stderr)
        return None

    def get_next_token(self) -> None:
        self._current_token = self._lexer.try_get_next_token()

    def parse_expression(self) -> Optional[ExprAst]:
        pass

    # number
    def parse_number_expression(self) -> ExprAst:
        assert self._current_token
        assert self._current_token.value()

        expr = NumberExprAst(value=float(self._current_token.value()))

        # Consume number and move to next token
        self.get_next_token()

        return expr

    # '(' expression ')'
    def parse_parentheses_expression(self) -> Optional[ExprAst]:
        self.get_next_token()  # eat (

        v: Optional[ExprAst] = self.parse_expression()

        if not v:
            return None

        if self._current_token.value() != ")":
            return self.empty_expression(reason="expected ')'")

        self.get_next_token()  # eat )

        return v

    def parse_identifier_expression(self) -> Optional[ExprAst]:
        assert self._current_token
        assert self._current_token.value()

        identifier: str = self._current_token.value()

        self.get_next_token()

        # Simple variable
        if self._current_token.value() != "(":
            return VariableExprAst(name=identifier)

        # Function call
        self.get_next_token()

        args: Sequence[ExprAst] = []
        if self._current_token.value() != ")":
            while True:
                arg: Optional[ExprAst] = self.parse_expression()

                if not arg:
                    return self.empty_expression(reason="")

                args.append(arg)

                if self._current_token.value() == ")":
                    break

                if self._current_token.value() != ",":
                    return self.empty_expression(reason="Expected ')' or ',' in argument list")

                self.get_next_token()  # eat ,

            self.get_next_token()  # eat )

        return CallExprAst(callee=identifier, args=args)

    def parse_primary(self) -> Optional[ExprAst]:
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

    def parse_expression(self) -> Optional[ExprAst]:
        lhs: Optional[ExprAst] = self.parse_primary()

        if not lhs:
            return None

        return self.parse_binary_op_rhs(expression_precedence=0, lhs=lhs)

    def parse_binary_op_rhs(self, expression_precedence: int, lhs: ExprAst) -> Optional[ExprAst]:
        pass
