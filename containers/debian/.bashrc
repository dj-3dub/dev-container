# Load bash completion
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi

# Set the Pro Prompt: [user@toolbox]:[directory]$
export PS1="\[\e[32m\]\u@toolbox\[\e[m\]:\[\e[34m\]\w\[\e[m\]\\$ "

# Useful aliases for your toolbox
alias ll='ls -lah'
alias grep='grep --color=auto'
