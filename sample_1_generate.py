from core.cociniinet import CoCiNiiNet

net = CoCiNiiNet(
        "https://cir.nii.ac.jp/crid/1420001326209796096",
        "津川翔", 
        wait_seconds=0.5,
        is_nayose=True,
     )
net.generate()
net.write_graphml("result.graphml")