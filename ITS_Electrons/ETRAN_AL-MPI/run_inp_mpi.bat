Remove-Item *.out
for %%f in (*.inp) do (
    echo %%~nf
    mkdir %%~nf
    Copy-Item itstigp2_mpi.exe ./%%~nf
    Copy-Item fort.11 ./%%~nf
    cd ./%%~nf
    mpiexec -n 32 itstigp2_mpi.exe "../%%~nf.inp" "../data_%%~nf.out"
    cd ../
    Remove-Item -r %%~nf
)