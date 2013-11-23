pkgname=sysql
pkgver=0.1
pkgrel=1
pkgdesc="Use sql queries against output of linux commands"
url=""
arch=('x86_64' 'i686')
license=('GPLv3')
depends=('python3')
optdepends=()
makedepends=()
conflicts=()
replaces=()
backup=()
install='sysql.install'
source=("http://www.server.tld/${pkgname}-${pkgver}.tar.gz"
        "foo.desktop")
md5sums=('a0afa52d60cea6c0363a2a8cb39a4095'
         'a0afa52d60cea6c0363a2a8cb39a4095')

build() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  cmake ./ -DCMAKE_INSTALL_PREFIX=/usr
  make
}

package() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  make DESTDIR="${pkgdir}" install
  install -Dm644 COPYING "$pkgdir/usr/share/licenses/$pkgname/COPYING"
}

# vim:set ts=2 sw=2 et: