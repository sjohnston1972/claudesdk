import asyncio
import sys
import time
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk import TextBlock, ToolUseBlock, ToolResultBlock

# ANSI color codes for PowerShell
class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

# Emoji shortcuts
EMOJIS = {
    'network': '🌐',
    'cisco': '🔷',
    'thinking': '🤔',
    'success': '✅',
    'running': '⚡',
    'tool': '🔧',
    'warning': '⚠️',
    'info': 'ℹ️',
    'wave': '👋',
    'chat': '💬',
    'brain': '🧠',
    'rocket': '🚀',
    'exit': '🚪',
    'prompt': '❯',
}

def print_animated_header():
    """Animated header on startup"""
    header = f"{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.RESET}"
    print(header)
    
    title = f"{Colors.CYAN}{EMOJIS['network']} Network Engineering Assistant {EMOJIS['cisco']}{Colors.RESET}"
    print(f"  {title}")
    
    subtitle = f"{Colors.CYAN}{EMOJIS['brain']} Powered by Claude Agent SDK {EMOJIS['rocket']}{Colors.RESET}"
    print(f"  {subtitle}")
    
    footer = f"{Colors.CYAN}{Colors.BOLD}═══════════════════════════════════════════════════════════════{Colors.RESET}"
    print(footer)
    print()

def print_typing_animation(text, delay=0.02):
    """Print text with typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_thinking():
    """Show thinking animation"""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    for _ in range(8):
        for char in spinner:
            print(f"\r{Colors.YELLOW}{char} Thinking...{Colors.RESET}", end='', flush=True)
            time.sleep(0.1)

def print_status(emoji, status, color=Colors.WHITE):
    """Print a status line"""
    print(f"{color}{emoji} {status}{Colors.RESET}")

def print_tool_execution(tool_name, command):
    """Print tool execution info"""
    print(f"\n{Colors.GREEN}{EMOJIS['running']} {Colors.BOLD}Running Tool: {tool_name}{Colors.RESET}")
    print(f"{Colors.MAGENTA}└─ Command: {command}{Colors.RESET}")

def print_tool_output(output):
    """Print tool output with formatting"""
    print(f"{Colors.DIM}{Colors.YELLOW}Output:{Colors.RESET}")
    # Indent the output for readability
    lines = output.split('\n')
    for line in lines[:20]:  # Limit to first 20 lines
        print(f"  {Colors.DIM}{line}{Colors.RESET}")
    if len(lines) > 20:
        print(f"  {Colors.YELLOW}... ({len(lines) - 20} more lines){Colors.RESET}")
    print()

def print_separator():
    """Print a nice separator"""
    print(f"{Colors.CYAN}{'=' * 62}{Colors.RESET}")

async def main():
    print_animated_header()
    
    print(f"{Colors.BOLD}Welcome to your Network Engineering Assistant!{Colors.RESET}")
    print(f"Type {Colors.BOLD}'exit'{Colors.RESET} to quit, or ask anything about your network.")
    print()
    print_separator()
    print()

    # Store conversation history
    conversation_history = []

    while True:
        # Get user input
        loop = asyncio.get_event_loop()
        try:
            user_input = await loop.run_in_executor(
                None, 
                lambda: input(f"{Colors.BOLD}{Colors.CYAN}{EMOJIS['prompt']} You:{Colors.RESET} ").strip()
            )
        except EOFError:
            break
        
        if user_input.lower() == "exit":
            print()
            print_status(EMOJIS['exit'], "Goodbye! Thanks for using the Network Engineering Assistant!", Colors.CYAN)
            break
        
        if not user_input:
            continue

        # Add user message to history
        conversation_history.append(f"User: {user_input}")

        print()
        print_thinking()
        print("\r" + " " * 50 + "\r", end='', flush=True)  # Clear the thinking animation
        
        print(f"{Colors.BOLD}{Colors.GREEN}{EMOJIS['chat']} Assistant:{Colors.RESET}", end=" ", flush=True)

        # Build the prompt with conversation context
        context = "\n".join(conversation_history[-10:])
        
        options = ClaudeAgentOptions(
            allowed_tools=["Bash"],
            permission_mode="bypassPermissions",
            system_prompt="""You are a network engineering assistant specializing in Cisco enterprise networking.
Your role is to help with network diagnostics, configuration analysis, and troubleshooting.
When running commands, always explain what you're looking for and what the results mean.
Be concise but thorough in your explanations.
Format output in a way that's easy for a network engineer to understand."""
        )

        # Send message and get response
        full_response = ""
        first_block = True
        
        async for message in query(
            prompt=context,
            options=options
        ):
            if hasattr(message, 'content'):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        if first_block:
                            print()  # Newline after "Assistant:"
                            first_block = False
                        # Use typing animation for text
                        print_typing_animation(block.text, delay=0.01)
                        full_response += block.text
                    
                    elif isinstance(block, ToolUseBlock):
                        print_tool_execution(block.name, block.input.get('command', str(block.input)))
                    
                    elif isinstance(block, ToolResultBlock):
                        print_tool_output(block.content)
        
        # Add assistant response to history
        conversation_history.append(f"Assistant: {full_response}")
        
        print()
        print_separator()
        print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print()
        print_status(EMOJIS['warning'], "Interrupted by user", Colors.YELLOW)
        sys.exit(0)