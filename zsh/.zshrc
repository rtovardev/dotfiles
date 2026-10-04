# Mantener cerca del principio: inicio rápido de Powerlevel10k.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

typeset -g DOTFILES_DIR="${${(%):-%N}:A:h:h}"
source "$DOTFILES_DIR/zsh/environment.zsh"
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git)

# Las completions personales se agregan antes del compinit de Oh My Zsh.
[[ ! -d "$HOME/.zsh/completions" ]] || fpath=("$HOME/.zsh/completions" $fpath)
if [[ -r "$ZSH/oh-my-zsh.sh" ]]; then
  source "$ZSH/oh-my-zsh.sh"
else
  autoload -Uz compinit
  compinit
fi

source "$DOTFILES_DIR/zsh/integrations.zsh"
source "$DOTFILES_DIR/zsh/aliases.zsh"

if [[ -n ${SSH_CONNECTION:-} ]]; then
  export EDITOR=vim
elif (( $+commands[nvim] )); then
  export EDITOR=nvim
elif (( $+commands[hx] )); then
  export EDITOR=hx
else
  export EDITOR=vim
fi
export VISUAL="$EDITOR"

unsetopt inc_append_history share_history
[[ ! -r "$HOME/.p10k.zsh" ]] || source "$HOME/.p10k.zsh"
[[ ! -r "$HOME/.config/zsh/local.zsh" ]] || source "$HOME/.config/zsh/local.zsh"

# Una sola instalación, después de los widgets de Atuin y otras integraciones.
if [[ -r "${ZSH_CUSTOM:-$ZSH/custom}/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
  source "${ZSH_CUSTOM:-$ZSH/custom}/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
elif [[ -r "${HOMEBREW_PREFIX:-/opt/homebrew}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
  source "${HOMEBREW_PREFIX:-/opt/homebrew}/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi

# Aliases
alias codex="codex --yolo"
alias agy="agy --dangerously-skip-permissions"
alias opencode="opencode --yolo"
