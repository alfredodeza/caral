from caral import util



describe "browsing the PyPi index skips some files":

    before each:
        self.browse = util.BrowsePyPi('', '')


    it "should skip htm files":
        pkg = "foobar.htm"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip html files":
        pkg = "foobar.html"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip org files":
        pkg = "foobar.org"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip net files":
        pkg = "foobar.net"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should skip http files":
        pkg = "http://foobar.me"

        assert self.browse.should_skip_pkg(pkg) is True

    it "should not skip files with http that are non urls":
        pkg = "httplib"

        assert self.browse.should_skip_pkg(pkg) is False

    it "should not skip files with https that are non urls":
        pkg = "httpslib"

        assert self.browse.should_skip_pkg(pkg) is False


describe "browsing PyPi index and grabs package files":

    before each:
        self.browse = util.BrowsePyPi('', '')

    it "does not skip tar.gz urls":
        href = "http://example.com/file.tar.gz"

        assert self.browse.package_from_url(href) == 'file.tar.gz'

    it "does not skip .tar.bz2 urls":
        href = "http://example.com/file.tar.bz2"

        assert self.browse.package_from_url(href) == 'file.tar.bz2'

    it "does not skip .tar urls":
        href = "http://example.com/file.tar"

        assert self.browse.package_from_url(href) == 'file.tar'

    it "does not skip .zip urls":
        href = "http://example.com/file.zip"

        assert self.browse.package_from_url(href) == 'file.zip'

    it "does not skip .tgz urls":
        href = "http://example.com/file.tgz"

        assert self.browse.package_from_url(href) == 'file.tgz'

    it "does skip non compressed file urls":
        href = "http://example.com/file.bar"

        assert self.browse.package_from_url(href) is False

    it "does not skip when is valid but has trailing slashes":
        href = "http://example.com/file.zip/"

        assert self.browse.package_from_url(href) == 'file.zip'

    it "removes trailing slashes":
        url = "http://example.com/bar/"
        assert self.browse.url_end_part(url) == 'bar'

    it "removes hashes from checksums from urls":
        url = "http://example.com/bar/package.tar#md5sdaf90987asdf0978"
        assert self.browse.url_end_part(url) == 'package.tar'

    it "removes hashes from checksums from urls with trailing slashes":
        url = "http://example.com/bar/package.tar#md5sdaf90987asdf0978/"
        assert self.browse.url_end_part(url) == 'package.tar'

