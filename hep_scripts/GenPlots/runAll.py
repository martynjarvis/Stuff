import ROOT

filenames = ["wm_lhc7_ct66_05","wm_lhc7_ct66_20","wm_lhc7_ct66_35","wp_lhc7_ct66_05","wp_lhc7_ct66_20","wp_lhc7_ct66_35","wm_lhc7_ct66_06","wm_lhc7_ct66_21","wm_lhc7_ct66_36","wp_lhc7_ct66_06","wp_lhc7_ct66_21","wp_lhc7_ct66_36","wm_lhc7_ct66_07","wm_lhc7_ct66_22","wm_lhc7_ct66_37","wp_lhc7_ct66_07","wp_lhc7_ct66_22","wp_lhc7_ct66_37","wm_lhc7_ct66_08","wm_lhc7_ct66_23","wm_lhc7_ct66_38","wp_lhc7_ct66_08","wp_lhc7_ct66_23","wp_lhc7_ct66_38","wm_lhc7_ct66_09","wm_lhc7_ct66_24","wm_lhc7_ct66_39","wp_lhc7_ct66_09","wp_lhc7_ct66_24","wp_lhc7_ct66_39","wm_lhc7_ct66_10","wm_lhc7_ct66_25","wm_lhc7_ct66_40","wp_lhc7_ct66_10","wp_lhc7_ct66_25","wp_lhc7_ct66_40","wm_lhc7_ct66_11","wm_lhc7_ct66_26","wm_lhc7_ct66_41","wp_lhc7_ct66_11","wp_lhc7_ct66_26","wp_lhc7_ct66_41","wm_lhc7_ct66_12","wm_lhc7_ct66_27","wm_lhc7_ct66_42","wp_lhc7_ct66_12","wp_lhc7_ct66_27","wp_lhc7_ct66_42","wm_lhc7_ct66_13","wm_lhc7_ct66_28","wm_lhc7_ct66_43","wp_lhc7_ct66_13","wp_lhc7_ct66_28","wp_lhc7_ct66_43","wm_lhc7_ct66_14","wm_lhc7_ct66_29","wm_lhc7_ct66_44","wp_lhc7_ct66_14","wp_lhc7_ct66_29","wp_lhc7_ct66_44","wm_lhc7_ct66_00","wm_lhc7_ct66_15","wm_lhc7_ct66_30","wp_lhc7_ct66_00","wp_lhc7_ct66_15","wp_lhc7_ct66_30","wm_lhc7_ct66_01","wm_lhc7_ct66_16","wm_lhc7_ct66_31","wp_lhc7_ct66_01","wp_lhc7_ct66_16","wp_lhc7_ct66_31","wm_lhc7_ct66_02","wm_lhc7_ct66_17","wm_lhc7_ct66_32","wp_lhc7_ct66_02","wp_lhc7_ct66_17","wp_lhc7_ct66_32","wm_lhc7_ct66_03","wm_lhc7_ct66_18","wm_lhc7_ct66_33","wp_lhc7_ct66_03","wp_lhc7_ct66_18","wp_lhc7_ct66_33","wm_lhc7_ct66_04","wm_lhc7_ct66_19","wm_lhc7_ct66_34","wp_lhc7_ct66_04","wp_lhc7_ct66_19","wp_lhc7_ct66_34"]

for file in filenames:
  f = ROOT.TFile.Open(file+".root") 
  t = f.Get('h10')
  t.Process("h10.C+",file)
  f.Close()




