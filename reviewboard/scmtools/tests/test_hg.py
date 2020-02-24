from djblets.testing.decorators import add_fixtures
from reviewboard.scmtools.hg import HgDiffParser, HgGitDiffParser, HgTool
from reviewboard.testing.testcase import TestCase
            self.tool.parse_diff_revision(filename=b'/dev/null',
                                          revision=b'bf544ea505f8')[1],
            PRE_CREATION)
        self.assertEqual(file.orig_filename, b'readme')
        self.assertEqual(file.orig_file_details, PRE_CREATION)
        self.assertEqual(file.orig_filename, b'empty')
        self.assertEqual(file.modified_file_details, b'4960455a8e88')
        self.assertEqual(file.modified_filename, b'empty')
        self.assertEqual(file.orig_file_details, b'356a6127ef19')
        self.assertEqual(file.orig_filename, b'empty')
        self.assertEqual(file.modified_file_details, b'4960455a8e88')
        self.assertEqual(file.modified_filename, b'empty')
        self.assertEqual(file.orig_file_details, b'bf544ea505f8')
        self.assertEqual(file.orig_filename, b'readme')
        self.assertEqual(file.modified_file_details, b'Uncommitted')
        self.assertEqual(file.modified_filename, b'readme')
        self.assertEqual(file.orig_file_details, b'356a6127ef19')
        self.assertEqual(file.orig_filename, b'readme')
        self.assertEqual(file.modified_file_details, b'4960455a8e88')
        self.assertEqual(file.modified_filename, b'readme')
        self.assertEqual(file.orig_file_details, b'356a6127ef19')
        self.assertEqual(file.orig_filename, b'readme')
        self.assertEqual(file.modified_file_details, b'4960455a8e88')
        self.assertEqual(file.modified_filename, b'readme')
        self.assertEqual(file.orig_file_details, b'bf544ea505f8')
        self.assertEqual(file.orig_filename, b'path/to file/readme.txt')
        self.assertEqual(file.modified_file_details, b'4960455a8e88')
        self.assertEqual(file.modified_filename, b'new/path to/readme.txt')
        self.assertEqual(file.orig_file_details, b'bf544ea505f8')
        self.assertEqual(file.orig_filename, 'réadme'.encode('utf-8'))
        self.assertEqual(file.modified_file_details, b'Uncommitted')
        self.assertEqual(file.modified_filename, 'réadme'.encode('utf-8'))
        self.assertEqual(file.orig_file_details, b'bf544ea505f8')
        self.assertEqual(file.orig_filename,
                         'path/to file/réadme.txt'.encode('utf-8'))
        self.assertEqual(file.modified_file_details, b'4960455a8e88')
        self.assertEqual(file.modified_filename,
                         'new/path to/réadme.txt'.encode('utf-8'))
            self.tool.parse_diff_revision(filename=b'doc/readme',
                                          revision=b'bf544ea505f8'),
            (b'doc/readme', b'bf544ea505f8'))
            self.tool.parse_diff_revision(filename=b'/dev/null',
                                          revision=b'bf544ea505f8'),
            (b'/dev/null', PRE_CREATION))
        self.assertNotIn(b'goodbye', value.diff)
        self.assertIn(b'goodbye', value.diff)
        old_tz = os.environ[str('TZ')]
        os.environ[str('TZ')] = str('US/Pacific')
            os.environ[str('TZ')] = old_tz
        tool = self.tool
        value = tool.get_file('doc/readme', Revision('661e5dd3c493'))
        self.assertIsInstance(value, bytes)
        with self.assertRaises(FileNotFoundError):
            tool.get_file('')
        with self.assertRaises(FileNotFoundError):
            tool.get_file('hello', PRE_CREATION)
    def test_file_exists(self):
        """Testing HgTool.file_exists"""
        rev = Revision('661e5dd3c493')

        self.assertTrue(self.tool.file_exists('doc/readme', rev))
        self.assertFalse(self.tool.file_exists('doc/readme2', rev))


class HgAuthFormTests(TestCase):
    """Unit tests for HgTool's authentication form."""

    def test_fields(self):
        """Testing HgTool authentication form fields"""
        form = HgTool.create_auth_form()

        self.assertEqual(list(form.fields), ['username', 'password'])
        self.assertEqual(form['username'].help_text, '')
        self.assertEqual(form['username'].label, 'Username')
        self.assertEqual(form['password'].help_text, '')
        self.assertEqual(form['password'].label, 'Password')

    @add_fixtures(['test_scmtools'])
    def test_load(self):
        """Tetting HgTool authentication form load"""
        repository = self.create_repository(
            tool_name='Mercurial',
            username='test-user',
            password='test-pass')

        form = HgTool.create_auth_form(repository=repository)
        form.load()

        self.assertEqual(form['username'].value(), 'test-user')
        self.assertEqual(form['password'].value(), 'test-pass')

    @add_fixtures(['test_scmtools'])
    def test_save(self):
        """Tetting HgTool authentication form save"""
        repository = self.create_repository(tool_name='Mercurial')

        form = HgTool.create_auth_form(
            repository=repository,
            data={
                'username': 'test-user',
                'password': 'test-pass',
            })
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(repository.username, 'test-user')
        self.assertEqual(repository.password, 'test-pass')


class HgRepositoryFormTests(TestCase):
    """Unit tests for HgTool's repository form."""

    def test_fields(self):
        """Testing HgTool repository form fields"""
        form = HgTool.create_repository_form()

        self.assertEqual(list(form.fields), ['path', 'mirror_path'])
        self.assertEqual(form['path'].help_text,
                         'The path to the repository. This will generally be '
                         'the URL you would use to check out the repository.')
        self.assertEqual(form['path'].label, 'Path')
        self.assertEqual(form['mirror_path'].help_text, '')
        self.assertEqual(form['mirror_path'].label, 'Mirror Path')

    @add_fixtures(['test_scmtools'])
    def test_load(self):
        """Tetting HgTool repository form load"""
        repository = self.create_repository(
            tool_name='Mercurial',
            path='https://hg.example.com/repo',
            mirror_path='https://hg.mirror.example.com/repo')

        form = HgTool.create_repository_form(repository=repository)
        form.load()

        self.assertEqual(form['path'].value(), 'https://hg.example.com/repo')
        self.assertEqual(form['mirror_path'].value(),
                         'https://hg.mirror.example.com/repo')

    @add_fixtures(['test_scmtools'])
    def test_save(self):
        """Tetting HgTool repository form save"""
        repository = self.create_repository(tool_name='Mercurial')

        form = HgTool.create_repository_form(
            repository=repository,
            data={
                'path': 'https://hg.example.com/repo',
                'mirror_path': 'https://hg.mirror.example.com/repo',
            })
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(repository.path, 'https://hg.example.com/repo')
        self.assertEqual(repository.mirror_path,
                         'https://hg.mirror.example.com/repo')