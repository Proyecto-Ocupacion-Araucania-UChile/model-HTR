binary file : `ketos compile -f xml -o dataset.arrow --random-split 0.8 0.1 0.1 `

Skratch `ketos train --augment --workers 4 -f binary --min-epochs 20 -w 0 -r 0.0001 dataset.arrow 
`


#Segmentation

finetuning `ketos segtrain --resize both -i modelsegpec_4902.mlmodel -f alto --workers 4 --min-epochs 20 --augment -t ./**/*.xml -p 0.90 -d cpu


if use --resize add : `RuntimeError: The size of tensor a (20) must match the size of tensor b (21) at 
non-singleton dimension 0
`