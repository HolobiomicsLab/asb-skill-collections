# Evaluation Strategy

## Direct Checks

- verify file exists: MSMetaEnhancer source code repository contains ConverterBuilder class definition
- script_runs: instantiate ConverterBuilder and execute automatic discovery of all WebConverter and ComputeConverter subclasses without errors
- output_matches_reference: generated Job list (source → target conversion pairs) can be enumerated from discovered converters
- verify field_present: each Job object in enumerated list contains source identifier, target identifier, and reference to conversion function
- script_runs: call get_conversion_functions on instantiated converter objects and verify returned functions match Job specifications, robust to order of discovery

## Expert Review

- verify that all converter subclasses discovered by ConverterBuilder are legitimate WebConverter or ComputeConverter implementations (no false positives from parent or abstract classes)
- verify that Job enumeration is complete: no supported converter classes are overlooked by the discovery mechanism
- verify that conversion function references in Job objects are callable and semantically correspond to declared source→target pairs
