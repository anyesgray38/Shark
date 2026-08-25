# Shark Routing Policy

## Default research route
`orchestrator -> research -> analyst -> validator -> reporter`

## Signal route
`orchestrator -> research -> analyst -> validator -> signal`

The Signal Agent is blocked unless the Validator returns `PASS`.

## Design route
`validated requirement -> design -> Penpot specification -> implementation -> design validation`

## Combined route
`research -> analyst -> validator -> signal -> reporter -> design`

Design may consume validated requirements and presentation needs, but must never change research conclusions.

## Failure propagation
A failed or conditional upstream artifact cannot be silently promoted downstream.
