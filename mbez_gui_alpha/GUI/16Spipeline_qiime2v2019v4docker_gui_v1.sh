docker run --rm -i -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-path manifest-data \
  --output-path paired-end-demux.qza \
  --input-format PairedEndFastqManifestPhred33V2

docker run --rm -i -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime demux summarize \
  --i-data paired-end-demux.qza \
  --o-visualization paired-end-demux.qzv

# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime dada2 denoise-paired \
#   --i-demultiplexed-seqs paired-end-demux.qza \
#   --p-trim-left-f 0 \
#   --p-trim-left-r 0 \
#   --p-trunc-len-f 300 \
#   --p-trunc-len-r 300 \
#   --o-table table.qza \
#   --o-representative-sequences rep-seqs.qza \
#   --o-denoising-stats denoising-stats.qza
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime feature-table summarize \
#   --i-table table.qza \
#   --o-visualization table.qzv \
#   --m-sample-metadata-file sample-metadata.tsv
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime feature-table tabulate-seqs \
#   --i-data rep-seqs.qza \
#   --o-visualization rep-seqs.qzv
# 
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime phylogeny align-to-tree-mafft-fasttree \
#     --i-sequences rep-seqs.qza \
#     --o-alignment aligned-rep-seqs.qza \
#     --o-masked-alignment masked-aligned-rep-seqs.qza \
#     --o-tree unrooted-tree.qza \
#     --o-rooted-tree rooted-tree.qza
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime diversity core-metrics-phylogenetic \
#       --i-phylogeny rooted-tree.qza \
#       --i-table table.qza \
#       --p-sampling-depth 1500 \
#       --m-metadata-file sample-metadata.tsv \
#       --output-dir core-metrics-results
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime diversity alpha-group-significance \
#         --i-alpha-diversity core-metrics-results/faith_pd_vector.qza \
#         --m-metadata-file sample-metadata.tsv \
#         --o-visualization core-metrics-results/faith-pd-group-significance.qzv
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime diversity alpha-group-significance \
#         --i-alpha-diversity core-metrics-results/evenness_vector.qza \
#         --m-metadata-file sample-metadata.tsv \
#         --o-visualization core-metrics-results/evenness-group-significance.qzv
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime diversity beta-group-significance \
#   --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
#   --m-metadata-file sample-metadata.tsv \
#   --m-metadata-column Layer \
#   --o-visualization core-metrics-results/unweighted-unifrac-layer-significance.qzv \
#   --p-pairwise
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime diversity beta-group-significance \
#   --i-distance-matrix core-metrics-results/unweighted_unifrac_distance_matrix.qza \
#   --m-metadata-file sample-metadata.tsv \
#   --m-metadata-column Site \
#   --o-visualization core-metrics-results/unweighted-unifrac-site-significance.qzv \
#   --p-pairwise
#
#   docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime diversity alpha-rarefaction \
#   --i-table table.qza \
#   --i-phylogeny rooted-tree.qza \
#   --p-max-depth 4000 \
#   --m-metadata-file sample-metadata.tsv \
#   --o-visualization alpha-rarefaction.qzv
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime feature-classifier classify-sklearn \
#   --i-classifier silva-132-99-nb-classifier.qza \
#   --i-reads rep-seqs.qza \
#   --o-classification taxonomy.qza
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime metadata tabulate \
#   --m-input-file taxonomy.qza \
#   --o-visualization taxonomy.qzv
#
# docker run --rm -it -u $(id -u):$(id -g) -v $(pwd):/data qiime2/core:2019.4 qiime taxa barplot \
#     --i-table table.qza \
#     --i-taxonomy taxonomy.qza \
#     --m-metadata-file sample-metadata.tsv \
#     --o-visualization taxa-bar-plots.qzv
