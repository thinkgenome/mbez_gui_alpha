git clone https://github.com/pereiramemo/BiG-MEx.git
export PATH=$PATH:"$PWD"/BiG-MEx

while IFS=' ' read -r col1 col2 col3; do run_bgc_dom_annot.bash $col2 $col3 $col1.bigmex_dom_annot --intype dna --nslots 2 --overwrite t --verbose t; done < $1

while IFS=' ' read -r col1 col2 col3; do cp $col1.bigmex_dom_annot/pe_bgc_dom.gz $col1.pe_bgc_dom.gz; done < $1

while IFS=' ' read -r col1 col2 col3; do run_bgc_dom_div.bash meta  $col1.pe_bgc_dom.gz  $col2 $col3  $col1.bigmex_dom_div_$2 --blast t  --plot_tree t  --only_rep t  --coverage t  --nslots 2  --verbose t  --domains $2  --overwrite t; done < $1

# ./run_bgc_dom_div.bash merge nr1.bigmex_dom_div_AMP_binding,nr2.bigmex_dom_div_AMP_binding,nr3.bigmex_dom_div_AMP_binding,nr4.bigmex_dom_div_AMP_binding,nr5.bigmex_dom_div_AMP_binding,nr6.bigmex_dom_div_AMP_binding,nr7.bigmex_dom_div_AMP_binding out_dom_merged_div_osd_AMP_binding --domain AMP-binding --num_iter 50 --sample_increment 20 --plot_rare_curve t --plot_tree t --only_rep t --nslots 20 --verbose t 2>&1 | tee bgc_dom_div_merge_AMP-binding_sample1234567.log

myarr=($(cat $1 | awk '{ print $1 }'))
cnt=${#myarr[@]}
for ((i=0;i<cnt;i++)); do
    myarr[i]="${myarr[i]}.bigmex_dom_div_$2"
    echo "${myarr[i]}"
done

str=$(IFS=$','; echo "${myarr[*]}" )

run_bgc_dom_div.bash merge ${str} out_dom_merged_div_$2 --domain $2 --num_iter 50 --sample_increment 20 --plot_rare_curve t --plot_tree t --only_rep t --nslots 2 --verbose t 2>&1 | tee bgc_dom_div_merge_$2.log
