# Tool Lifecycle

## Purpose

Manage public presentation, deletion, sharing, and student favorites safely.

## Requirements

### Requirement: Independent tool visibility states

The system SHALL manage plaza listing, sharing, and deletion independently for each tool.

#### Scenario: Plaza unlist preserves share

- **WHEN** an administrator unlists a tool with an active unexpired share
- **THEN** the tool is absent from the plaza and remains available through its share preview

### Requirement: Safe public previews

The system SHALL return only public presentation fields from plaza and share endpoints.

#### Scenario: Share preview

- **WHEN** an unauthenticated visitor opens an active share link
- **THEN** the response excludes prompt templates and internal interface configuration

### Requirement: Recoverable tool deletion

The system SHALL soft-delete teacher tools and allow authorized administrators to restore them.

#### Scenario: Teacher deletes own tool

- **WHEN** a teacher deletes an owned tool
- **THEN** normal tool lists exclude it while historical records and an administrator restoration path remain available

### Requirement: Student favorites

The system SHALL allow authenticated students to add, remove, and list their own favorites.

#### Scenario: Favorite isolation

- **WHEN** a student lists favorites
- **THEN** only that student's favorite tools are returned in descending favorite time
