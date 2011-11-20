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


describe "browsing PyPi index skips some urls":

    before each:
        self.browse = util.BrowsePyPi('', '')

    it "does not skip tar.gz urls":
        href = "http://example.com/file.tar.gz"

        assert self.browse.should_skip_href(href) is False

    it "does not skip .tar.bz2 urls":
        href = "http://example.com/file.tar.bz2"

        assert self.browse.should_skip_href(href) is False

    it "does not skip .tar urls":
        href = "http://example.com/file.tar"

        assert self.browse.should_skip_href(href) is False

    it "does not skip .zip urls":
        href = "http://example.com/file.zip"

        assert self.browse.should_skip_href(href) is False

    it "does not skip .tgz urls":
        href = "http://example.com/file.tgz"

        assert self.browse.should_skip_href(href) is False

    it "does skip non compressed file urls":
        href = "http://example.com/file.bar"

        assert self.browse.should_skip_href(href) is True

    it "does not skip when is valid but has trailing slashes":
        href = "http://example.com/file.zip/"

        assert self.browse.should_skip_href(href) is False


