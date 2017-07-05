#!/bin/sh
#
# To run as an executable on a unix platform, do the following:
# chmod 775 wget_data.bat
# ./wget_data.bat
#
wget -x "https://irsa.ipac.caltech.edu:443/data/Herschel/MESS/images/RTVIR-1_160_pixfrac10.0.mod.fits"
wget -x "https://irsa.ipac.caltech.edu:443/data/Herschel/MESS/images/RTVIR-all_160_pixfrac10.0.mod.fits"
wget -x "https://irsa.ipac.caltech.edu:443/data/Herschel/MESS/images/RTVIR-1_70_pixfrac10.0.mod.fits"
wget -x "https://irsa.ipac.caltech.edu:443/data/Herschel/MESS/images/RTVIR_70_pixfrac10.0.mod.fits"
wget -x "https://irsa.ipac.caltech.edu:443/data/Herschel/MESS/images/RTVIR_160_pixfrac10.0.mod.fits"
wget -x "https://irsa.ipac.caltech.edu:443/data/Herschel/MESS/images/RTVIR-all_70_pixfrac10.0.mod.fits"
