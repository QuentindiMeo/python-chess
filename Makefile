##
## PERSONAL PROJECT, 2021
## chess
## File description:
## Makefile
##

CP	=	cp -f
RM	=	rm -rf
CHMOD	=	chmod 777
ECHO	=	/bin/echo -e

SRC	=	chess.py
NAME	=	Chess
CACHE	=	__pycache__ .ipynb_checkpoints

all: $(NAME)

$(NAME):
	@$(CP) $(SRC) $(NAME)
	@$(CHMOD) $(NAME)
	@$(ECHO) $(GRN) " [OK]" $(BLU)$(SRC)$(DEF)
	@$(ECHO) $(NAME)" rendered "$(BOLDGRN)"successfully"$(DEF)"!"

clean:
	@$(RM) $(NAME)
	@$(RM) $(CACHE)
	@$(ECHO) "Cleaned "$(NAME)

fclean:	clean

re: fclean all

.PHONY: clean fclean re Chess

DEF	=	"\033[00m"
BLU	=	"\033[1;34m"
GRN	=	"\033[0;32m"
BOLDGRN	=	"\033[1;32m"
RED	=	"\033[1;31m"
