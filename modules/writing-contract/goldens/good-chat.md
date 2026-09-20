The body text is now 16px, so the chat should look closer to the browser example.

That size is locked in pixels on purpose. A relative `rem` value shrank against Kilo’s smaller root, which is why the last pass looked tiny. **The takeaway is bigger prose, not a new theme.**

Headings stay a step above the body, and fenced code wraps instead of scrolling off the side. If a paragraph still feels cramped, that is a writing problem, not a missing design-token dump.
