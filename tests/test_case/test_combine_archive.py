from biosimulators_test_suite.test_case import combine_archive
from biosimulators_test_suite.test_case.published_project import SimulatorCanExecutePublishedProject
from biosimulators_test_suite.warnings import TestCaseWarning
from biosimulators_utils.report.data_model import DataSetResults
from biosimulators_utils.report.io import ReportWriter
from biosimulators_utils.sedml.data_model import Report, DataSet
import numpy
import os
import shutil
import tempfile
import unittest


class CombineArchiveTestCaseTest(unittest.TestCase):
    IMAGE = 'ghcr.io/biosimulators/biosimulators_copasi/copasi:latest'
    CURATED_ARCHIVE_FILENAME = os.path.join(
        os.path.dirname(__file__), '..', '..',
        'examples', 'sbml-core', 'Ciliberto-J-Cell-Biol-2003-morphogenesis-checkpoint.omex')

    def setUp(self):
        self.dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def test_WhenACombineArchiveHasAMasterFileSimulatorOnlyExecutesThisFile_eval_outputs(self):
        case = combine_archive.WhenACombineArchiveHasAMasterFileSimulatorOnlyExecutesThisFile()
        case._expected_report_ids = [
            'a.sedml/b',
        ]

        with self.assertRaisesRegex(ValueError, 'did not generate'):
            case.eval_outputs(None, None, None, self.dirname)

        report = Report(data_sets=[DataSet(id='A', label='A'), DataSet(id='B', label='B')])
        data = DataSetResults({
            'A': numpy.array([1, 2, 3]),
            'B': numpy.array([4, 5, 6]),
        })
        ReportWriter().run(report, data, self.dirname, 'a.sedml/b')
        case.eval_outputs(None, None, None, self.dirname)

        ReportWriter().run(report, data, self.dirname, 'b.sedml/b')
        with self.assertWarnsRegex(TestCaseWarning, ''):
            case.eval_outputs(None, None, None, self.dirname)

    def test_WhenACombineArchiveHasAMasterFileSimulatorOnlyExecutesThisFile(self):
        specs = {'image': {'url': self.IMAGE}}
        curated_case = SimulatorCanExecutePublishedProject(filename=self.CURATED_ARCHIVE_FILENAME)

        # test synthetic case generated and used to test simulator
        case = combine_archive.WhenACombineArchiveHasAMasterFileSimulatorOnlyExecutesThisFile(
            published_projects_test_cases=[curated_case])
        case.eval(specs)

    def test_WhenACombineArchiveHasNoMasterFileSimulatorExecutesAllSedDocuments_eval_outputs(self):
        case = combine_archive.WhenACombineArchiveHasNoMasterFileSimulatorExecutesAllSedDocuments()
        case._expected_report_ids = [
            'a.sedml/b',
            'b.sedml/b',
        ]

        with self.assertRaisesRegex(ValueError, 'did not generate'):
            case.eval_outputs(None, None, None, self.dirname)

        report = Report(data_sets=[DataSet(id='A', label='A'), DataSet(id='B', label='B')])
        data = DataSetResults({
            'A': numpy.array([1, 2, 3]),
            'B': numpy.array([4, 5, 6]),
        })
        ReportWriter().run(report, data, self.dirname, 'a.sedml/b')
        ReportWriter().run(report, data, self.dirname, 'b.sedml/b')
        case.eval_outputs(None, None, None, self.dirname)

        ReportWriter().run(report, data, self.dirname, 'c.sedml/b')
        with self.assertWarnsRegex(TestCaseWarning, ''):
            case.eval_outputs(None, None, None, self.dirname)

    def test_WhenACombineArchiveHasNoMasterFileSimulatorExecutesAllSedDocuments(self):
        specs = {'image': {'url': self.IMAGE}}
        curated_case = SimulatorCanExecutePublishedProject(filename=self.CURATED_ARCHIVE_FILENAME)

        # test synthetic case generated and used to test simulator
        case = combine_archive.WhenACombineArchiveHasNoMasterFileSimulatorExecutesAllSedDocuments(
            published_projects_test_cases=[curated_case])
        case.eval(specs)
