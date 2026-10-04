if (( $+commands[wtp] )); then
  eval "$(wtp shell-init zsh)"
fi
if (( $+commands[atuin] )); then
  eval "$(atuin init zsh)"
fi
[[ ! -r "$HOME/.bun/_bun" ]] || source "$HOME/.bun/_bun"

# Ruta del archivo público; los datos y plugins de Herdr permanecen fuera.
export HERDR_CONFIG_PATH="$HOME/.config/herdr/config.toml"
