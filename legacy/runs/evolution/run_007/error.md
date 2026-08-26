# Cycle 007 failed

- Type: `RuntimeError`
- Message: candidate_guide failed after 3 attempts: attempt 1: RuntimeError: LM Studio HTTP 500: {
  "error": {
    "message": "Engine protocol predict request returned 400: {\"error\":{\"code\":400,\"message\":\"request (15333 tokens) exceeds the available context size (8192 tokens), try increasing it\",\"type\":\"exceed_context_size_error\",\"n_prompt_tokens\":15333,\"n_ctx\":8192}}",
    "type": "internal_error",
    "code": "unknown",
    "param": null
  }
} | attempt 2: RuntimeError: LM Studio HTTP 500: {
  "error": {
    "message": "Engine protocol predict request returned 400: {\"error\":{\"code\":400,\"message\":\"request (15488 tokens) exceeds the available context size (8192 tokens), try increasing it\",\"type\":\"exceed_context_size_error\",\"n_prompt_tokens\":15488,\"n_ctx\":8192}}",
    "type": "internal_error",
    "code": "unknown",
    "param": null
  }
} | attempt 3: RuntimeError: LM Studio HTTP 500: {
  "error": {
    "message": "Engine protocol predict request returned 400: {\"error\":{\"code\":400,\"message\":\"request (15488 tokens) exceeds the available context size (8192 tokens), try increasing it\",\"type\":\"exceed_context_size_error\",\"n_prompt_tokens\":15488,\"n_ctx\":8192}}",
    "type": "internal_error",
    "code": "unknown",
    "param": null
  }
}

See `error.json` for the traceback.
