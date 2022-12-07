from core.cociniinet import CoCiNiiNet

if __name__ == "__main__":
    net = CoCiNiiNet("https://cir.nii.ac.jp/crid/1070012545625749888", "田村匠", 0.5)
    net.generate(max_reqests=500)
    net.write_graphml("takumi500.graphml")
