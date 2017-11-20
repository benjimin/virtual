# Virtual products for the OpenDataCube

## Useful applications for virtual products:

 - Rasterfile product (not needing to index).
 - Shapefile product (encapsulating rasterisation).
 - Band math (simple computations on the fly, without needing to store).
 - Composite products (handling join and ensuring mutual availability,
   e.g., bands from NBAR together with from PQ)
   and grouped products (e.g. Landsat 5, 7 & 8).
 - Masked products (encapsulating boilerplate and topic expertise), e.g.
   cloud-free imagery.
 - Temporal clustering (reconstituting satellite passes
   to avoid duplicate observations).
 - Complex filtering (beyond any API limitations, perhaps even accessing
   external metadata, e.g. filtering by quality scores)
 - Locally cached products.
 - As a flexible base from which to prototype/refactor datacube concepts
   (not constrained to reflect entrenched structure of data holdings)
   
