# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the methylKit package support storing methylation data in tabix-indexed bgzipped files on disk, and if so, how are the database path and metadata header configured?: 'We can now create a `methylRawListDB` object, which stores the same content as *myobj* from above. But the single `methylRaw` objects retrieve their data from the tabix-file linked under `dbpath`.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk. The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage.: 'myobjDB=methRead(file.list,
           sample.id=list("test1","test2","ctrl1","ctrl2"),
           assembly="hg18",
           treatment=c(1,1,0,0),
           context="CpG",
           dbtype ='

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Example CpG methylation call files in methylKit-compatible format (e.g., from bisulfite sequencing via Bismark): 'Using the same example CpG files'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylRawListDB object with dbpath slot populated and pointing to bgzipped tabix files on disk: 'methylRawListDB object stored as bgzipped tabix files on disk. Verify that the dbpath slot is populated'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Tabix file header containing methylKit metadata and version information (≥ 1.13.1): 'the tabix file header contains the expected methylKit metadata (version >= 1.13.1 behaviour)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] methylKit: 'title: "methylKit: User Guide v`r packageVersion('methylKit')`"'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'packageVersion('methylKit')'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version-specific behavior changes or tabix feature introduction timeline: '_No changelog found._'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No methods section provided describing methRead() function signature, dbtype parameter options, or dbpath slot initialization: 'Document contains only vignette header and setup code, no methods section text'
