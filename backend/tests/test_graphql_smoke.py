from __future__ import annotations

from src.api.schema import schema


def test_graphql_schema_contains_minimum_contract() -> None:
    schema_sdl = schema.as_str()

    assert "type Query" in schema_sdl
    assert "type Mutation" in schema_sdl
    assert "getAnalysisById" in schema_sdl
    assert "listAnalyses" in schema_sdl
    assert "myAnalyses" in schema_sdl
    assert "me" in schema_sdl
    assert "getSystemStats" in schema_sdl
    assert "uploadRadiography" in schema_sdl
    assert "registerUser" in schema_sdl
    assert "loginUser" in schema_sdl
