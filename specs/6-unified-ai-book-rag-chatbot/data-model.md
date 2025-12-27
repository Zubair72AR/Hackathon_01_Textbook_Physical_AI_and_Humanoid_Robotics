# Data Model: Unified AI/Spec-Driven Book with Integrated RAG Chatbot

## Core Entities

### BookContent
- **id**: UUID (primary key)
- **module_id**: UUID (foreign key to Module)
- **chapter_id**: UUID (foreign key to Chapter)
- **section_id**: UUID (foreign key to Section)
- **title**: String (max 255)
- **content**: Text (markdown content)
- **word_count**: Integer
- **created_at**: DateTime
- **updated_at**: DateTime
- **version**: Integer

**Validation rules**:
- Title must not be empty
- Content must be valid markdown
- Word count must be non-negative

### Module
- **id**: UUID (primary key)
- **title**: String (max 255)
- **description**: Text
- **order**: Integer
- **created_at**: DateTime
- **updated_at**: DateTime

**Validation rules**:
- Title must not be empty
- Order must be unique within the book
- Description must not exceed 1000 characters

### Chapter
- **id**: UUID (primary key)
- **module_id**: UUID (foreign key to Module)
- **title**: String (max 255)
- **description**: Text
- **order**: Integer
- **word_count**: Integer
- **created_at**: DateTime
- **updated_at**: DateTime

**Validation rules**:
- Title must not be empty
- Order must be unique within module
- Module_id must reference existing module

### Section
- **id**: UUID (primary key)
- **chapter_id**: UUID (foreign key to Chapter)
- **title**: String (max 255)
- **description**: Text
- **order**: Integer
- **word_count**: Integer
- **created_at**: DateTime
- **updated_at**: DateTime

**Validation rules**:
- Title must not be empty
- Order must be unique within chapter
- Chapter_id must reference existing chapter

### Embedding
- **id**: UUID (primary key)
- **content_id**: UUID (foreign key to BookContent)
- **vector**: JSON (embedding vector)
- **chunk_text**: Text (the text chunk that was embedded)
- **chunk_index**: Integer
- **created_at**: DateTime

**Validation rules**:
- Content_id must reference existing BookContent
- Vector must be a valid embedding array
- Chunk_index must be non-negative

### UserSession
- **id**: UUID (primary key)
- **user_id**: UUID
- **created_at**: DateTime
- **updated_at**: DateTime
- **expires_at**: DateTime

**Validation rules**:
- Expires_at must be in the future
- User_id must be valid if provided

### Query
- **id**: UUID (primary key)
- **session_id**: UUID (foreign key to UserSession)
- **query_text**: Text
- **response_text**: Text
- **sources**: JSON (list of source references)
- **created_at**: DateTime

**Validation rules**:
- Query_text must not be empty
- Session_id must reference existing UserSession

### SourceReference
- **id**: UUID (primary key)
- **content_id**: UUID (foreign key to BookContent)
- **start_char**: Integer
- **end_char**: Integer
- **confidence_score**: Float (0.0-1.0)

**Validation rules**:
- Content_id must reference existing BookContent
- Start_char must be less than end_char
- Confidence_score must be between 0.0 and 1.0

## Relationships

- Module (1) → (Many) Chapter
- Chapter (1) → (Many) Section
- Section (1) → (Many) BookContent
- BookContent (1) → (Many) Embedding
- UserSession (1) → (Many) Query
- Query (Many) → (Many) SourceReference (via junction)
- BookContent (1) → (Many) SourceReference

## State Transitions

### BookContent
- DRAFT → REVIEW → APPROVED → PUBLISHED
- APPROVED → ARCHIVED (when content is deprecated)

### UserSession
- ACTIVE → EXPIRED (when expires_at is reached)
- ACTIVE → ENDED (when explicitly ended by user)