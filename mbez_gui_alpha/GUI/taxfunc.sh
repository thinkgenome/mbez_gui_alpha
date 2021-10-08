while IFS=' ' read -r col1 col2 col3; do cat $col2 $col3 > $col1.r1andr2reads.fastq.gz; done < $1
while IFS=' ' read -r col1 col2 col3; do docker run -t -u $(id -u):$(id -g) -v $(pwd):/data buchfink/diamond diamond blastx -d /data/bacteria.nr.part.fasta.dmnd -q /data/$col1.r1andr2reads.fastq.gz -o /data/$col1.r1andr2reads.fastq.gz.daa -f 100 ; done < $1
docker image load -i megan6.18.5.tar
while IFS=' ' read -r col1 col2 col3; do docker run -t -u $(id -u):$(id -g) -v $(pwd):/data megan6.18.5 /megan/tools/daa-meganizer -i /data/$col1.r1andr2reads.fastq.gz.daa --mapDB /data/megan-map-Oct2019.db -a2t -a2seed; done < $1
