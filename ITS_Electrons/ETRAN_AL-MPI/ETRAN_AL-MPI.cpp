#include <fstream>
#include <sstream>
#include <iostream>
#include <iomanip>

using namespace std;

const int spec_size = 49;
const int n_files = 1;
const int hist_per_batch = 40000;
const int batches = 32000;

double al_thicknesses[n_files] = {
	2.0
};

double spectrum[spec_size] = {
	1.00000000000000E+00,
	9.99992267054338E-01,
	9.99982984595934E-01,
	9.99971841659110E-01,
	9.99958459503615E-01,
	9.99942392943543E-01,
	9.99923097124499E-01,
	9.99899934168167E-01,
	9.99872106726653E-01,
	9.99838671271615E-01,
	9.99798498226869E-01,
	9.99750218811864E-01,
	9.99692171885152E-01,
	9.99622377366130E-01,
	9.99538429921982E-01,
	9.99437419232894E-01,
	9.99315850257263E-01,
	9.99169404027326E-01,
	9.98993057251350E-01,
	9.98780564037495E-01,
	9.98524216689449E-01,
	9.98214978597741E-01,
	9.97843680261586E-01,
	9.97422149008085E-01,
	9.96942942923556E-01,
	9.96374035200908E-01,
	9.95685525294102E-01,
	9.94850967831306E-01,
	9.93837405766220E-01,
	9.92603775682282E-01,
	9.91098117075041E-01,
	9.89256243438998E-01,
	9.86994433245243E-01,
	9.84206373441190E-01,
	9.80752528145321E-01,
	9.76449507341925E-01,
	9.71051462096900E-01,
	9.63974999534183E-01,
	9.54470612633045E-01,
	9.41907067643762E-01,
	9.24990003151106E-01,
	9.02717418634458E-01,
	8.71580983358500E-01,
	8.27049103456778E-01,
	7.64257956773509E-01,
	6.69107774709549E-01,
	5.28641653981050E-01,
	3.18008918546167E-01,
	0.00000000000000E+00
};

double energy[spec_size] = {
	9.9999619,
	8.2540117,
	6.8128970,
	5.6233945,
	4.6415742,
	3.8311755,
	3.1622690,
	2.6101506,
	2.1544294,
	1.7782755,
	1.4677963,
	1.2115254,
	0.9999984,
	0.8254030,
	0.6812912,
	0.5623407,
	0.4641584,
	0.3831184,
	0.3162276,
	0.2610156,
	0.2154434,
	0.1778279,
	0.1467800,
	0.1211528,
	0.1000001,
	0.0825405,
	0.0681292,
	0.0562342,
	0.0464159,
	0.0383119,
	0.0316228,
	0.0261016,
	0.0215443,
	0.0177828,
	0.0146780,
	0.0121153,
	0.0100000,
	0.0082540,
	0.0068129,
	0.0056234,
	0.0046416,
	0.0038312,
	0.0031623,
	0.0026102,
	0.0021544,
	0.0017783,
	0.0014678,
	0.0012115,
	0.0010000
};


int main(int argc, char const *argv[])
{
	int i, j;

	string base_name_inp = "ETRAN_AL-MPI";
	string extention_inp = ".inp";
	//string base_name_out = "al_dose_";
	//string extention_out = ".out";
	string file_name;

	ofstream file;
	//ifstream inpfile;

	for (i = 1; i <= n_files; ++i)
	{
		if (i < 10)
			file_name = base_name_inp + to_string(0)+ to_string(i)+ extention_inp;
		else 
			file_name = base_name_inp + to_string(i)+ extention_inp;

		file.open(file_name);
		//cout << file_name << endl;

		file << "ECHO 1\n";
		file << "TITLE\n";
		file << "AL dose with L2-CPE V1.1 environment\n";
		file << "GEOMETRY 1\n\n";
		file << "1 50 " << setprecision(2) << scientific << al_thicknesses[i-1] << " * Al shielding (cm)\n";
		//file << "4 1 0.0254 * 30 mils Si\n\n";
		file << "SPECTRUM " << spec_size << endl;
		file << "* CDF converted from FluenceConversionExercise20180430.xlsx by Brandon Phillips EM41\n";
		file << "* Normalization constant = 1.1287419285E+14 for 15 year fluence\n";
		for (j = 0; j < spec_size; ++j)
			file << setprecision(10) << scientific << spectrum[j] << endl;

		file << "* energy (MeV)\n";
		for (int j = 0; j < spec_size; ++j)
			file << setprecision(7) << fixed << energy[j] << endl;
		
		file << "\nDIRECTION\n";
		//file << " ISOTROPIC\n";
		file << " COSINE-LAW\n";
		file << "CUTOFFS 0.002 0.002 * electron and photons cut-offs (MeV)\n\n";
		file << "* run size options\n";
		file << "HISTORIES-PER-BATCH " << hist_per_batch * i * i << endl;
		file << "BATCHES " << batches;
		file.close();
	}

	return 0;
}