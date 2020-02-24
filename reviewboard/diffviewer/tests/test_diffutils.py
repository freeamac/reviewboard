from django.utils import six
from reviewboard.deprecation import RemovedInReviewBoard50Warning
    convert_line_endings,
    convert_to_unicode,
    get_filediffs_match,
    get_filediff_encodings,
    split_line_endings,
    _PATCH_GARBAGE_INPUT,
from reviewboard.diffviewer.errors import PatchError
from reviewboard.diffviewer.models import DiffCommit, FileDiff
    _CUMULATIVE_DIFF = {
        'parent': b''.join(
            parent_diff
            for parent_diff in (
                entry['parent']
                for entry in _COMMITS
            )
            if parent_diff is not None
        ),
        'diff': (
            b'diff --git a/qux b/qux\n'
            b'new file mode 100644\n'
            b'index 000000..03b37a0\n'
            b'--- /dev/null\n'
            b'+++ /b/qux\n'
            b'@@ -0,0 +1 @@\n'
            b'foo bar baz qux\n'

            b'diff --git a/bar b/quux\n'
            b'index 5716ca5..e69de29 100644\n'
            b'--- a/bar\n'
            b'+++ b/quux\n'
            b'@@ -1 +0,0 @@\n'
            b'-bar\n'

            b'diff --git a/baz b/baz\n'
            b'index 7601807..280beb2 100644\n'
            b'--- a/baz\n'
            b'+++ b/baz\n'
            b'@@ -1 +1 @@\n'
            b'-baz\n'
            b'+baz baz baz\n'

            b'diff --git a/corge b/corge\n'
            b'index e69de29..f248ba3 100644\n'
            b'--- a/corge\n'
            b'+++ b/corge\n'
            b'@@ -0,0 +1 @@\n'
            b'+corge\n'
        ),
    }

        self.spy_on(Repository.get_file,
                    owner=Repository,
                    call_fake=get_file)
                    owner=Repository,
        self.filediffs = list(FileDiff.objects.all())
        self.diffset.finalize_commit_series(
            cumulative_diff=self._CUMULATIVE_DIFF['diff'],
            parent_diff=self._CUMULATIVE_DIFF['parent'],
            validation_info=None,
            validate=False,
            save=True)

            diff=b'diff1')
            diff=b'diff2')
            diff=b'diff3')
            diff=b'diff4')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'interdiff2')
            diff=b'interdiff3')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
        """Testing get_diff_files for a diffset with history"""
        result = get_diff_files(diffset=self.diffset)
        self.assertEqual(len(result), len(self.diffset.cumulative_files))
            [diff_file['filediff'].pk for diff_file in result],
            [
                filediff.pk
                for filediff in get_sorted_filediffs(
                    self.diffset.cumulative_files)
            ])
        for diff_file in result:
            self.assertIsNone(diff_file['base_filediff'])
        """Testing get_diff_files query count for a diffset with history"""
        with self.assertNumQueries(3):
        self.assertIsNone(f['base_filediff'])
        self.assertIsNone(f['base_filediff'])

    def test_get_diff_files_with_history_base_commit(self):
        """Testing get_diff_files for a whole diffset with history with a
        specified base commit ID
        """
        self.set_up_filediffs()

        review_request = self.create_review_request(repository=self.repository,
                                                    create_with_history=True)
        review_request.diffset_history.diffsets = [self.diffset]

        with self.assertNumQueries(len(self.filediffs) + 2):
            files = get_diff_files(diffset=self.diffset,
                                   base_commit=DiffCommit.objects.get(pk=2))

        expected_results = self._get_filediff_base_mapping_from_details(
            self.get_filediffs_by_details(),
            [
                (
                    (4, 'bar', '5716ca5', 'quux', 'e69de29'),
                    (2, 'bar', '8e739cc', 'bar', '0000000'),
                ),
                (
                    (3, 'corge', 'PRE-CREATION', 'corge', 'f248ba3'),
                    None,
                ),
                (
                    (3, 'foo', '257cc56', 'qux', '03b37a0'),
                    (2, 'foo', 'e69de29', 'foo', '257cc56'),
                ),
            ])

        results = {
            f['filediff']: f['base_filediff']
            for f in files
        }

        self.assertEqual(results, expected_results)

    def test_get_diff_files_with_history_base_commit_as_latest(self):
        """Testing get_diff_files for a whole diffset with history with a
        specified base commit as the latest commit
        """
        self.set_up_filediffs()

        review_request = self.create_review_request(repository=self.repository,
                                                    create_with_history=True)
        review_request.diffset_history.diffsets = [self.diffset]

        files = get_diff_files(diffset=self.diffset,
                               base_commit=DiffCommit.objects.get(pk=4))

        self.assertEqual(files, [])

    def test_get_diff_files_with_history_tip_commit(self):
        """Testing get_diff_files for a whole diffset with history with a
        specified tip commit
        """
        self.set_up_filediffs()

        review_request = self.create_review_request(repository=self.repository,
                                                    create_with_history=True)
        review_request.diffset_history.diffsets = [self.diffset]

        with self.assertNumQueries(3 + len(self.filediffs)):
            files = get_diff_files(diffset=self.diffset,
                                   tip_commit=DiffCommit.objects.get(pk=3))

        expected_results = self._get_filediff_base_mapping_from_details(
            self.get_filediffs_by_details(),
            [
                (
                    (3, 'foo', '257cc56', 'qux', '03b37a0'),
                    None,
                ),
                (
                    (2, 'baz', 'PRE-CREATION', 'baz', '280beb2'),
                    None,
                ),
                (
                    (3, 'corge', 'PRE-CREATION', 'corge', 'f248ba3'),
                    None,
                ),
                (
                    (3, 'bar', 'PRE-CREATION', 'bar', '5716ca5'),
                    None,
                ),
            ])

        results = {
            f['filediff']: f['base_filediff']
            for f in files
        }

        self.assertEqual(results, expected_results)

    def test_get_diff_files_with_history_tip_commit_precomputed(self):
        """Testing get_diff_files for a whole diffset with history with a
        specified tip commit when ancestors have been precomputed
        """
        self.set_up_filediffs()

        review_request = self.create_review_request(repository=self.repository,
                                                    create_with_history=True)
        review_request.diffset_history.diffsets = [self.diffset]

        for f in self.filediffs:
            f.get_ancestors(minimal=False, filediffs=self.filediffs)

        with self.assertNumQueries(4):
            files = get_diff_files(diffset=self.diffset,
                                   tip_commit=DiffCommit.objects.get(pk=3))

        expected_results = self._get_filediff_base_mapping_from_details(
            self.get_filediffs_by_details(),
            [
                (
                    (3, 'foo', '257cc56', 'qux', '03b37a0'),
                    None,
                ),
                (
                    (2, 'baz', 'PRE-CREATION', 'baz', '280beb2'),
                    None,
                ),
                (
                    (3, 'corge', 'PRE-CREATION', 'corge', 'f248ba3'),
                    None,
                ),
                (
                    (3, 'bar', 'PRE-CREATION', 'bar', '5716ca5'),
                    None,
                ),
            ])

        results = {
            f['filediff']: f['base_filediff']
            for f in files
        }

        self.assertEqual(results, expected_results)

    def test_get_diff_files_with_history_base_tip(self):
        """Testing get_diff_files for a whole diffset with history with a
        specified base and tip commit
        """
        self.set_up_filediffs()

        review_request = self.create_review_request(repository=self.repository,
                                                    create_with_history=True)
        review_request.diffset_history.diffsets = [self.diffset]

        with self.assertNumQueries(2 + len(self.filediffs)):
            files = get_diff_files(diffset=self.diffset,
                                   base_commit=DiffCommit.objects.get(pk=2),
                                   tip_commit=DiffCommit.objects.get(pk=3))

        expected_results = self._get_filediff_base_mapping_from_details(
            self.get_filediffs_by_details(),
            [
                (
                    (3, 'foo', '257cc56', 'qux', '03b37a0'),
                    (2, 'foo', 'e69de29', 'foo', '257cc56'),
                ),
                (
                    (3, 'corge', 'PRE-CREATION', 'corge', 'f248ba3'),
                    None,
                ),
                (
                    (3, 'bar', 'PRE-CREATION', 'bar', '5716ca5'),
                    (2, 'bar', '8e739cc', 'bar', '0000000'),
                ),
            ])

        results = {
            f['filediff']: f['base_filediff']
            for f in files
        }

        self.assertEqual(results, expected_results)

    def test_get_diff_files_with_history_base_tip_ancestors_precomputed(self):
        """Testing get_diff_files for a whole diffset with history with a
        specified base and tip commit when ancestors are precomputed
        """
        self.set_up_filediffs()

        review_request = self.create_review_request(repository=self.repository,
                                                    create_with_history=True)
        review_request.diffset_history.diffsets = [self.diffset]

        for f in self.filediffs:
            f.get_ancestors(minimal=False, filediffs=self.filediffs)

        with self.assertNumQueries(4):
            files = get_diff_files(diffset=self.diffset,
                                   base_commit=DiffCommit.objects.get(pk=2),
                                   tip_commit=DiffCommit.objects.get(pk=3))

        expected_results = self._get_filediff_base_mapping_from_details(
            self.get_filediffs_by_details(),
            [

                (
                    (3, 'foo', '257cc56', 'qux', '03b37a0'),
                    (2, 'foo', 'e69de29', 'foo', '257cc56'),
                ),
                (
                    (3, 'corge', 'PRE-CREATION', 'corge', 'f248ba3'),
                    None,
                ),
                (
                    (3, 'bar', 'PRE-CREATION', 'bar', '5716ca5'),
                    (2, 'bar', '8e739cc', 'bar', '0000000'),
                ),
            ])

        results = {
            f['filediff']: f['base_filediff']
            for f in files
        }

        self.assertEqual(results, expected_results)

    def _get_filediff_base_mapping_from_details(self, by_details, details):
        """Return a mapping from FileDiffs to base FileDiffs from the details.

        Args:
            by_details (dict):
                A mapping of FileDiff details to FileDiffs, as returned from
                :py:meth:`BaseFileDiffAncestorTests.get_filediffs_by_details`.

            details (list):
                A list of the details in the form of:

                .. code-block:: python

                   [
                       (filediff_1_details, parent_1_details),
                       (filediff_2_details, parent_2_details),
                   ]

                where each set of details is either ``None`` or a 5-tuple of:

                - :py:attr`FileDiff.commit_id`
                - :py:attr`FileDiff.source_file`
                - :py:attr`FileDiff.source_revision`
                - :py:attr`FileDiff.dest_file`
                - :py:attr`FileDiff.dest_detail`

        Returns:
            dict:
            A mapping of the FileDiffs to their base FileDiffs (or ``None`` if
            there is no base FileDiff).
        """
        return {
            by_details[filediff_details]:
                by_details.get(base_filediff_details)
            for filediff_details, base_filediff_details in details
        }


class GetFileDiffsMatchTests(TestCase):
    """Unit tests for get_filediffs_match."""

    fixtures = ['test_scmtools', 'test_users']

    def setUp(self):
        super(GetFileDiffsMatchTests, self).setUp()

        review_request = self.create_review_request(create_repository=True)
        self.diffset = self.create_diffset(review_request)

    def test_with_filediff_none(self):
        """Testing get_filediffs_match with either filediff as None"""
        filediff = self.create_filediff(self.diffset, save=False)

        self.assertFalse(get_filediffs_match(filediff, None))
        self.assertFalse(get_filediffs_match(None, filediff))

        message = 'filediff1 and filediff2 cannot both be None'

        with self.assertRaisesMessage(ValueError, message):
            self.assertFalse(get_filediffs_match(None, None))

    def test_with_diffs_equal(self):
        """Testing get_filediffs_match with diffs equal"""
        filediff1 = self.create_filediff(self.diffset,
                                         diff=b'abc',
                                         save=False)
        filediff2 = self.create_filediff(self.diffset,
                                         diff=b'abc',
                                         save=False)

        self.assertTrue(get_filediffs_match(filediff1, filediff2))

    def test_with_deleted_true(self):
        """Testing get_filediffs_match with deleted flags both set"""
        self.assertTrue(get_filediffs_match(
            self.create_filediff(self.diffset,
                                 diff=b'abc',
                                 status=FileDiff.DELETED,
                                 save=False),
            self.create_filediff(self.diffset,
                                 diff=b'def',
                                 status=FileDiff.DELETED,
                                 save=False)))

    def test_with_sha256_equal(self):
        """Testing get_filediffs_match with patched SHA256 hashes equal"""
        filediff1 = self.create_filediff(self.diffset,
                                         diff=b'abc',
                                         save=False)
        filediff2 = self.create_filediff(self.diffset,
                                         diff=b'def',
                                         save=False)

        filediff1.extra_data['patched_sha256'] = 'abc123'
        filediff2.extra_data['patched_sha256'] = 'abc123'

        self.assertTrue(get_filediffs_match(filediff1, filediff2))

    def test_with_sha1_equal(self):
        """Testing get_filediffs_match with patched SHA1 hashes equal"""
        filediff1 = self.create_filediff(self.diffset,
                                         diff=b'abc',
                                         save=False)
        filediff2 = self.create_filediff(self.diffset,
                                         diff=b'def',
                                         save=False)

        filediff1.extra_data['patched_sha1'] = 'abc123'
        filediff2.extra_data['patched_sha1'] = 'abc123'

        self.assertTrue(get_filediffs_match(filediff1, filediff2))

    def test_with_sha1_not_equal(self):
        """Testing get_filediffs_match with patched SHA1 hashes not equal"""
        filediff1 = self.create_filediff(self.diffset,
                                         diff=b'abc',
                                         save=False)
        filediff2 = self.create_filediff(self.diffset,
                                         diff=b'def',
                                         save=False)

        filediff1.extra_data['patched_sha1'] = 'abc123'
        filediff2.extra_data['patched_sha1'] = 'def456'

        self.assertFalse(get_filediffs_match(filediff1, filediff2))

    def test_with_sha256_not_equal_and_sha1_equal(self):
        """Testing get_filediffs_match with patched SHA256 hashes not equal
        and patched SHA1 hashes equal
        """
        filediff1 = self.create_filediff(self.diffset,
                                         diff=b'abc',
                                         save=False)
        filediff2 = self.create_filediff(self.diffset,
                                         diff=b'def',
                                         save=False)

        filediff1.extra_data.update({
            'patched_sha256': 'abc123',
            'patched_sha1': 'abcdef',
        })
        filediff2.extra_data.update({
            'patched_sha256': 'def456',
            'patched_sha1': 'abcdef',
        })

        self.assertFalse(get_filediffs_match(filediff1, filediff2))
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'diff1')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'diff1')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'interdiff3')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'diff1')
            diff=b'diff2')
            diff=b'diff3')
            diff=b'diff1')
            diff=b'interdiff1')
            diff=b'interdiff2')
            diff=b'interdiff3')
            diff=b'interdiff4')
            diff=b'interdiff5')
            diff=b'diff1')
            diff=b'interdiff1')
            diff=b'diff2')
            diff=b'interdiff2')
            diff=b'diff3')
            diff=b'interdiff3')

        siteconfig_settings = {
            'diffviewer_syntax_highlighting': False,
        }

        with self.siteconfig_settings(siteconfig_settings,
                                      reload_settings=False):
            header = get_last_header_before_line(context=context,
                                                 filediff=filediff,
                                                 interfilediff=None,
                                                 target_line=line_number)
            chunks = get_file_chunks_in_range(
                context=context,
                filediff=filediff,
                interfilediff=None,
                first_line=1,
                num_lines=get_last_line_number_in_diff(
                    context=context,
                    filediff=filediff,
                    interfilediff=None))
        siteconfig_settings = {
            'diffviewer_syntax_highlighting': False,
        }

        with self.siteconfig_settings(siteconfig_settings,
                                      reload_settings=False):
            header = get_last_header_before_line(context=context,
                                                 filediff=filediff,
                                                 interfilediff=None,
                                                 target_line=line_number)
            chunks = get_file_chunks_in_range(
                context=context,
                filediff=filediff,
                interfilediff=None,
                first_line=1,
                num_lines=get_last_line_number_in_diff(
                    context=context,
                    filediff=filediff,
                    interfilediff=None))
        patched = patch(diff=diff,
                        orig_file=old,
                        filename='foo.c')
            patch(diff=diff,
                  orig_file=old,
                  filename='foo.c')
        patched = patch(diff=diff,
                        orig_file=old,
                        filename='test.c')
        patched = patch(diff=diff,
                        orig_file=old,
                        filename='README')
        patched = patch(diff=diff,
                        orig_file=old,
                        filename='README')
        patched = patch(diff=diff,
                        orig_file=old,
                        filename='README')
        patched = patch(diff=diff,
                        orig_file=old,
                        filename='README')
class GetFileDiffEncodingsTests(TestCase):
    """Unit tests for get_filediff_encodings."""

    fixtures = ['test_scmtools']

    def setUp(self):
        super(GetFileDiffEncodingsTests, self).setUp()

        self.repository = self.create_repository(encoding='ascii,iso-8859-15')
        self.diffset = self.create_diffset(repository=self.repository)

    def test_with_stored_encoding(self):
        """Testing get_filediff_encodings with recorded FileDiff.encoding"""
        filediff = self.create_filediff(self.diffset,
                                        encoding='utf-16')

        self.assertEqual(get_filediff_encodings(filediff),
                         ['utf-16', 'ascii', 'iso-8859-15'])

    def test_with_out_stored_encoding(self):
        """Testing get_filediff_encodings without recorded FileDiff.encoding"""
        filediff = self.create_filediff(self.diffset)

        self.assertEqual(get_filediff_encodings(filediff),
                         ['ascii', 'iso-8859-15'])

    def test_with_custom_encodings(self):
        """Testing get_filediff_encodings with custom encoding_list"""
        filediff = self.create_filediff(self.diffset)

        self.assertEqual(
            get_filediff_encodings(filediff,
                                   encoding_list=['rot13', 'palmos']),
            ['rot13', 'palmos'])


        self.set_up_filediffs()

        self.assertEqual(get_original_file(filediff=filediff), b'bar\n')
            filediff=filediff,
            request=None,
            encoding_list=None))
        self.set_up_filediffs()

        self.assertEqual(get_original_file(filediff=filediff), b'baz\n')
        self.set_up_filediffs()

        self.assertEqual(get_original_file(filediff=filediff), b'')
        self.set_up_filediffs()

        self.assertEqual(get_original_file(filediff=filediff), b'foo\n')
    def test_empty_parent_diff_old_patch(self):
        """Testing get_original_file with an empty parent diff with patch(1)
        that does not accept empty diffs
        """
        self.set_up_filediffs()

        # Older versions of patch will choke on an empty patch with a "garbage
        # input" error, but newer versions will handle it just fine. We stub
        # out patch here to always fail so we can test for the case of an older
        # version of patch without requiring it to be installed.
        def _patch(diff, orig_file, filename, request=None):
            raise PatchError(
                filename=filename,
                error_output=_PATCH_GARBAGE_INPUT,
                orig_file=orig_file,
                new_file='tmp123-new',
                diff=b'',
                rejects=None)

        self.spy_on(patch, call_fake=_patch)

            orig = get_original_file(filediff=filediff)
            orig = get_original_file(filediff=filediff)

    def test_empty_parent_diff_new_patch(self):
        """Testing get_original_file with an empty parent diff with patch(1)
        that does accept empty diffs
        """
        self.set_up_filediffs()

        filediff = (
            FileDiff.objects
            .select_related('parent_diff_hash',
                            'diffset',
                            'diffset__repository',
                            'diffset__repository__tool')
            .get(dest_file='corge',
                 dest_detail='f248ba3',
                 commit_id=3)
        )

        # FileDiff creation will set the _IS_PARENT_EMPTY flag.
        del filediff.extra_data[FileDiff._IS_PARENT_EMPTY_KEY]
        filediff.save(update_fields=('extra_data',))

        # Newer versions of patch will allow empty patches. We stub out patch
        # here to always fail so we can test for the case of a newer version
        # of patch without requiring it to be installed.
        def _patch(diff, orig_file, filename, request=None):
            # This is the only call to patch() that should be made.
            self.assertEqual(diff,
                             b'diff --git a/corge b/corge\n'
                             b'new file mode 100644\n'
                             b'index 0000000..e69de29\n')
            return orig_file

        self.spy_on(patch, call_fake=_patch)

        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff)

        self.assertEqual(orig, b'')

        # Refresh the object from the database with the parent diff attached
        # and then verify that re-calculating the original file does not cause
        # additional queries.
        filediff = (
            FileDiff.objects
            .select_related('parent_diff_hash')
            .get(pk=filediff.pk)
        )

        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff)
        self.set_up_filediffs()

            orig = get_original_file(filediff=filediff)

    def test_with_encoding_list(self):
        """Testing get_original_file with encoding_list is deprecated"""
        self.set_up_filediffs()

        filediff = FileDiff.objects.get(dest_file='bar',
                                        dest_detail='8e739cc',
                                        commit_id=1)

        message = (
            'The encoding_list parameter passed to get_original_file() is '
            'deprecated and will be removed in Review Board 5.0.'
        )

        with self.assert_warns(RemovedInReviewBoard50Warning, message):
            get_original_file(filediff, encoding_list=['ascii'])

    def test_with_filediff_with_encoding_set(self):
        """Testing get_original_file with FileDiff.encoding set"""
        content = 'hello world'.encode('utf-16')

        repository = self.create_repository()
        self.spy_on(repository.get_file,
                    call_fake=lambda *args, **kwargs: content)
        self.spy_on(convert_to_unicode)
        self.spy_on(convert_line_endings)

        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset,
                                        encoding='utf-16')

        self.assertEqual(get_original_file(filediff=filediff), content)
        self.assertTrue(convert_to_unicode.called_with(
            content, ['utf-16', 'iso-8859-15']))
        self.assertTrue(convert_line_endings.called_with('hello world'))

    def test_with_filediff_with_repository_encoding_set(self):
        """Testing get_original_file with Repository.encoding set"""
        content = 'hello world'.encode('utf-16')

        repository = self.create_repository(encoding='utf-16')
        self.spy_on(repository.get_file,
                    call_fake=lambda *args, **kwargs: content)
        self.spy_on(convert_to_unicode)
        self.spy_on(convert_line_endings)

        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)

        self.assertEqual(get_original_file(filediff=filediff), content)
        self.assertTrue(convert_to_unicode.called_with(content, ['utf-16']))
        self.assertTrue(convert_line_endings.called_with('hello world'))


class SplitLineEndingsTests(TestCase):
    """Unit tests for reviewboard.diffviewer.diffutils.split_line_endings."""

    def test_with_byte_string(self):
        """Testing split_line_endings with byte string"""
        lines = split_line_endings(
            b'This is line 1\n'
            b'This is line 2\r\n'
            b'This is line 3\r'
            b'This is line 4\r\r\n'
            b'This is line 5'
        )

        for line in lines:
            self.assertIsInstance(line, bytes)

        self.assertEqual(
            lines,
            [
                b'This is line 1',
                b'This is line 2',
                b'This is line 3',
                b'This is line 4',
                b'This is line 5',
            ])

    def test_with_unicode_string(self):
        """Testing split_line_endings with unicode string"""
        lines = split_line_endings(
            'This is line 1\n'
            'This is line 2\r\n'
            'This is line 3\r'
            'This is line 4\r\r\n'
            'This is line 5'
        )

        for line in lines:
            self.assertIsInstance(line, six.text_type)

        self.assertEqual(
            lines,
            [
                'This is line 1',
                'This is line 2',
                'This is line 3',
                'This is line 4',
                'This is line 5',
            ])