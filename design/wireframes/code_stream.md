# Wireframe: Code Stream Interface

## Layout Overview
The interface uses a vertically scrolling stream of "Activity Cards". Each card represents an agent step (e.g., Thought, Search, Edit).

```
+-----------------------------------------------------------------+
| [Logo] [Agent Name: Gemma4-Super]          [PAUSE] [STEP] [FEED] |
+-----------------------------------------------------------------+
|                                                                 |
| [ Activity Card #1 ]                                            |
| +-------------------------------------------------------------+ |
| | [Type: Reasoning] 12:45 PM                                  | |
| | "I need to investigate why the auth flow is failing..."      | |
| +-------------------------------------------------------------+ |
|                                                                 |
| [ Activity Card #2 ]                                            |
| +-------------------------------------------------------------+ |
| | [Type: File Edit] 12:46 PM                                  | |
| | File: src/auth.py                                           | |
| | [---] - return False                                        | |
| | [+++] + return user.is_authenticated                        | |
| +-------------------------------------------------------------+ |
|                                                                 |
| [ Current Step: Active... ]                                     |
| +-------------------------------------------------------------+ |
| | [Type: Thought] 12:47 PM                                    | |
| | "Applying the fix and running tests..."                     | |
| | [Spinner] [Step Indicator]                                  | |
| +-------------------------------------------------------------+ |
|                                                                 |
| [ Footer: Input Field for Feedback ]                            |
| +-------------------------------------------------------------+ |
| | [Type feedback to the agent here...]                  [Send] | |
| +-------------------------------------------------------------+ |
+-----------------------------------------------------------------+
```

## Key Components
1. **Header**: Contains global controls and agent status.
2. **Activity Card**: A container for a single unit of work. Supports multiple sub-types:
   - **Reasoning**: Textual thought process.
   - **Code/Diff**: Specialized visualization for file changes or output.
   - **Log**: Standard output/error from shell commands.
3. **Control Bar**: Floating or pinned bar with global agent controls.
4. **Feedback Input**: Always accessible input field to communicate with the agent.
