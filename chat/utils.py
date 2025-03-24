from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split
from scipy import stats
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class StreamingSeriesMatrixParser:
    def __init__(self, file_stream):
        self.file_stream = file_stream
        self.series_description = {}
        self.sample_ids = []
        self.phenotype_matrix = {}
        self.matrix_trigger = False
        self.matrix = []
        self.max_rows = 10000

    def run(self, description_ids, sample_id, phenotype_ids, matrix_start):
        logger.debug("Starting file parsing")
        for line in self.file_stream:
            try:
                line = line.decode('utf-8').replace('\n', '').split('\t')
                if not self.matrix_trigger:
                    self.get_descriptive_lines(line, description_ids)
                    self.get_sample_ids(line, sample_id)
                    self.get_phenotype_info(line, phenotype_ids)
                    self.get_matrix(line, matrix_start)
                elif len(self.matrix) < self.max_rows:
                    self.get_matrix(line)
                else:
                    break
            except Exception as e:
                logger.error(f"Error parsing line: {e}")
                raise

    def get_descriptive_lines(self, line, description_ids):
        if line[0] in description_ids:
            self.series_description[line[0]] = line[1:]

    def get_sample_ids(self, line, sample_id):
        if line[0] == sample_id:
            self.sample_ids = line[1:]

    def get_phenotype_info(self, line, phenotype_ids):
        if line[0] in phenotype_ids:
            label = line[1].split(':')[0].strip(' "')
            self.phenotype_matrix[label] = [p.split(':')[1].strip(' "') for p in line[1:]]

    def get_matrix(self, line, matrix_start=None):
        if self.matrix_trigger:
            self.matrix.append(line)
        elif line[0] == matrix_start:
            self.matrix_trigger = True


def train_epigenetic_clock(file_stream):
    parser = StreamingSeriesMatrixParser(file_stream)
    parser.run(
        description_ids=['!Series_title', '!Series_geo_accession', '!Series_pubmed_id', '!Series_summary', '!Series_overall_design', '!Series_sample_id', '!Series_relation'],
        sample_id='!Sample_geo_accession',
        phenotype_ids=['!Sample_characteristics_ch1'],
        matrix_start='!series_matrix_table_begin'
    )

    df = pd.DataFrame(data=parser.matrix[1:], columns=parser.matrix[0])
    df = df.set_index('"ID_REF"').apply(pd.to_numeric, errors='coerce').dropna(axis=0)

    ages = [int(x) for x in parser.phenotype_matrix.get('age', [])][:len(df.columns)]

    pca = PCA(n_components=4)
    pca_values = pca.fit_transform(df.values.T)
    pc1 = pca_values[:, 0]
    non_outlier_list = [label for x, label in zip(pc1, df.columns) if x < 5]
    non_outlier_ages = [age for x, age in zip(pc1, ages) if x < 5]

    X_train, X_test, y_train, y_test = train_test_split(
        df[non_outlier_list].values.T, non_outlier_ages, test_size=0.1, random_state=42
    )

    lasso_cv = LassoCV(cv=3, n_jobs=2)
    lasso_cv.fit(X_train, y_train)

    predicted_age = lasso_cv.predict(X_test)
    r2_score = stats.pearsonr(predicted_age, y_test)[0] ** 2

    return {
        "biological_age": predicted_age.tolist(),
        "actual_age": y_test,
        "r2_score": r2_score,
        "sample_ids": non_outlier_list[-len(y_test):]
    }
