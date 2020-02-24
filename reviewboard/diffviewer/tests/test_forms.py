from django.utils import six
from djblets.util.filesystem import is_exe_in_path
        self.repository = self.create_repository(tool_name='Git')
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                         self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                    self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
    def test_clean_no_committer(self):
        """Testing UploadCommitForm.clean when no committer_ fields are present
        """
        field_names = {
            'committer_date',
            'committer_email',
            'committer_name',
        }

        diff = SimpleUploadedFile('diff',
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                  content_type='text/x-patch')

        form_data = self._default_form_data.copy()

        for field in field_names:
            del form_data[field]

        form = UploadCommitForm(
            diffset=self.diffset,
            data=form_data,
            files={
                'diff': diff,
            })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            field: ['This field is required.']
            for field in field_names
        })

    def test_clean_commiter_unsupported(self):
        """Testing UploadCommitForm.clean when committer_ fields are present
        for a SCMTool that doesn't support them
        """
        if not is_exe_in_path('hg'):
            raise nose.SkipTest('Hg is not installed')

        self.repository.tool = Tool.objects.get(name='Mercurial')
        self.repository.save()

        diff = SimpleUploadedFile('diff',
                                  self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
                                  content_type='text/x-patch')

        form = UploadCommitForm(
            diffset=self.diffset,
            data=self._default_form_data.copy(),
            files={
                'diff': diff,
            })

        self.assertTrue(form.is_valid())

        self.assertNotIn('committer_date', form.cleaned_data)
        self.assertNotIn('committer_email', form.cleaned_data)
        self.assertNotIn('committer_name', form.cleaned_data)

        diff_file = SimpleUploadedFile('diff',
                                       self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
        diff_file = SimpleUploadedFile('diff',
                                       self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
        self.assertEqual(filediff.diff, self.DEFAULT_GIT_FILEDIFF_DATA_DIFF)
        if not is_exe_in_path('hg'):
            raise nose.SkipTest('Hg is not installed')

        self.assertEqual(f.source_revision, revisions[0].decode('utf-8'))
        self.assertEqual(f.dest_detail, revisions[1].decode('utf-8'))
        original_file = get_original_file(filediff=f,
                                          request=None,
                                          encoding_list=['ascii'])
        patched_file = get_patched_file(source_data=original_file,
                                        filediff=f)
        self.assertEqual(f.source_revision, revisions[0].decode('utf-8'))
        self.assertEqual(f.dest_detail, revisions[2].decode('utf-8'))
        original_file = get_original_file(filediff=f,
                                          request=None,
                                          encoding_list=['ascii'])
        patched_file = get_patched_file(source_data=original_file,
                                        filediff=f)
        self.diff = SimpleUploadedFile('diff',
                                       self.DEFAULT_GIT_FILEDIFF_DATA_DIFF,
        validation_info = self._base64_json({
        })
        validation_info = self._base64_json({
        })
        validation_info = self._base64_json({
        })
        validation_info = self._base64_json({
        })
        validation_info = base64.b64encode(b'Not valid json.')

        # Python 2 and 3 differ in the error contents you'll get when
        # attempting to load non-JSON data.
        if six.PY3:
            expected_error = 'Expecting value: line 1 column 1 (char 0)'
        else:
            expected_error = 'No JSON object could be decoded'

                'Could not parse validation info "%s": %s'
                % (validation_info.decode('utf-8'), expected_error),
            b'index %s..%s 100644\n'
        validation_info = self._base64_json({
        })
        validation_info = self._base64_json({
        })
            with self.siteconfig_settings({'diffviewer_max_diff_size': 1},
                                          reload_settings=False):

    def _base64_json(self, data):
        """Return a Base64-encoded JSON payload.

        Args:
            data (object):
                The data to encode to JSON.

        Returns:
            bytes:
            The Base64-encoded JSON payload.
        """
        return base64.b64encode(json.dumps(data).encode('utf-8'))