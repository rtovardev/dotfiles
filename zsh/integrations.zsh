if (( $+commands[wtp] )); then
  eval "$(wtp shell-init zsh)"
fi
if (( $+commands[atuin] )); then
  eval "$(atuin init zsh)"
fi
[[ ! -r "$HOME/.bun/_bun" ]] || source "$HOME/.bun/_bun"
