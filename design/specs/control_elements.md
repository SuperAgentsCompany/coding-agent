# Design Specs: Agentic Control Elements

## 1. Pause Button
- **Function**: Halts the agent's execution after the current tool call completes.
- **States**:
  - **Idle**: Label "Pause", Icon `pause-circle`.
  - **Pausing**: Label "Waiting to pause...", Spinner replaces icon.
  - **Paused**: Label "Resume", Icon `play-circle`, High-contrast color (e.g., `nova-color-warning`).
- **Interaction**: Single click to toggle. Immediate visual feedback is critical to confirm the signal was sent.

## 2. Step-through Mode Toggle
- **Function**: When enabled, the agent will pause and wait for user approval before *every* tool call or major decision.
- **Visual**: A toggle switch in the header.
- **Approval UI**:
  - When a step is pending: A "Proceed" button and a "Modify/Cancel" option appear in the current Activity Card.
  - Indicator: Pulsing glow on the active card to signal user input is required.

## 3. Feedback Injection
- **Function**: Allows the user to insert thoughts or constraints into the agent's working memory.
- **Input**: Multiline text area at the bottom of the stream.
- **Shortcut**: `Cmd+Enter` or `Ctrl+Enter` to send.
- **Visual Feedback**: The sent feedback appears as a "User Input" activity card in the stream, clearly distinguished from agent-generated cards.
- **Cues**: Visual indicator in the input area when the agent is "Listening" (processing input).

## 4. Visual Cues for "Agentic State"
- **Thinking**: Subtle pulsing background on the latest card.
- **Acting**: Progress bar or activity spinner on the specific tool being used.
- **Success/Failure**: Green/Red left-border accents on completed activity cards.
