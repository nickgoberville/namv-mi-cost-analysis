from distutils.core import setup

setup(name = "namv_mi",
    version = "0.1",
    description = "Cost model code",
    author = "Nick Goberville",
    author_email = "nicholas.a.goberville@wmich.edu",
    url = "Nan",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['namv_mi', 'namv_mi.cost_analysis'],
    package_dir={'namv_mi': 'src/modules/namv_mi', 'namv_mi.cost_analysis': 'src/modules/namv_mi/cost_analysis'})