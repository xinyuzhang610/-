## ADDED Requirements

### Requirement: Authorized tool conversation
The system SHALL require student authentication before AI interaction and SHALL reject private, deleted, expired, or inaccessible tools.

#### Scenario: Public preview attempts interaction
- **WHEN** an unauthenticated visitor sends a message from a share preview
- **THEN** the system returns an authentication requirement without creating a usage record

### Requirement: Contextual sessions
The system SHALL store conversation ownership and a bounded history used only by the owning user.

#### Scenario: Continue conversation
- **WHEN** a user sends a later message with an owned session identifier
- **THEN** recent messages from that session are included as context

### Requirement: Streaming conversation
The system SHALL expose SSE events named meta, delta, done, and error for streaming responses.

#### Scenario: Upstream stream completes
- **WHEN** DeepSeek completes a stream
- **THEN** the client receives deltas followed by done and the completed interaction is persisted once
