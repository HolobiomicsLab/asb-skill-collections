# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] How does the ConverterBuilder component automatically discover and instantiate all available converter classes to create a complete set of source-to-target conversion Job objects?: 'It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MSMetaEnhancer fetches metadata from multiple external services (CIR, CTS, PubChem, IDSM, and BridgeDb), which serve as the underlying converters that the ConverterBuilder must discover and instantiate into Job objects.: 'It adds metadata like SMILES, InChI, and CAS number fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MSMetaEnhancer source code package including libs/converters/web/ and libs/converters/compute/ directories: 'Converter Builder: Automatically discovers and instantiates available converters; Manages both web and compute converters'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] WebConverter and ComputeConverter base class definitions with conversion specifications: 'Base Converter Classes: Converter: Abstract base class for all converters; WebConverter: Base class for web-based API services; ComputeConverter: Base class for local computation services'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Enumerated list of Job objects (source_attribute, target_attribute, converter_name) representing all supported conversions: 'Job System: Job: Represents a conversion task (source → target using specific converter); Jobs are defined as tuples: (source_attribute, target_attribute, converter_name)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Test report (pytest output) verifying discovered jobs match converter-defined conversion methods: 'make sure the existing tests still work by running ``pytest``'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ConverterBuilder instantiation log or manifest showing all discovered converter classes and their conversion counts: 'Converter Builder: Automatically discovers and instantiates available converters'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pytest: 'make sure the existing tests still work by running ``pytest``'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Create a new Python file in `MSMetaEnhancer/libs/converters/web/` named after your service'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] MSMetaEnhancer: 'Converter Builder: Automatically discovers and instantiates available converters'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No explicit specification of which WebConverter and ComputeConverter subclasses are expected to be discovered: 'passed `multidict` instead of `frozendict` to `aiohttp.ClientSession.post` (required by package)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No description of the structure or interface of the Job class or object: 'take only first result when there are multiple hits in CIR conversions'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No specification of the exact format or naming convention for converter classes that should be auto-discovered: 'support `ISOMERIC_SMILES` and `CANONICAL_SMILES` in PubChem instead of generic `SMILES`'
