# Inicialización común a shells de login e interactivas; PATH sin duplicados.
typeset -U path PATH

if [[ -z ${HOMEBREW_PREFIX:-} ]]; then
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv zsh)"
  elif [[ -x /home/linuxbrew/.linuxbrew/bin/brew ]]; then
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv zsh)"
  fi
fi

if [[ -d "$HOME/.bun" ]]; then
  export BUN_INSTALL="$HOME/.bun"
fi
if [[ -d "$HOME/.dotnet" ]]; then
  export DOTNET_ROOT="$HOME/.dotnet"
fi
if [[ -d "$HOME/.railway" ]]; then
  export RAILWAY_HOME="$HOME/.railway"
fi
if [[ -d "${HOMEBREW_PREFIX:-/opt/homebrew}/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home" ]]; then
  export JAVA_HOME="${HOMEBREW_PREFIX:-/opt/homebrew}/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
fi

() {
  local directory
  local -a additions
  for directory in \
    "$HOME/bin" "$HOME/.local/bin" "$HOME/go/bin" \
    "$HOME/.antigravity-ide/antigravity-ide/bin" "$HOME/.mavis/bin" \
    "$HOME/.bun/bin" "$HOME/.composio" "$HOME/.atuin/bin" \
    "$HOME/.dotnet" "$HOME/.dotnet/tools" "$HOME/.cargo/bin" \
    "${HOMEBREW_PREFIX:-/opt/homebrew}/opt/rustup/bin" \
    "${JAVA_HOME:-$HOME/.no-java}/bin" "$HOME/.railway/bin"; do
    [[ ! -d "$directory" ]] || additions+=("$directory")
  done
  path=("${additions[@]}" "${path[@]}")
}
export PATH
export PANDOC_PDF_ENGINE=tectonic
