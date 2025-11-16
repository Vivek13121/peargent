import { Layout, Navbar, Footer } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import 'nextra-theme-docs/style.css'

const navbar = (
  <Navbar
    logo={
      <div className="flex items-center gap-2">
        <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded" />
        <span className="font-bold">Peargent</span>
      </div>
    }
    projectLink="https://github.com/yourusername/peargent"
  />
)

const footer = (
  <Footer>
    <span>
      MIT {new Date().getFullYear()} ©{' '}
      <a href="https://github.com/yourusername/peargent" target="_blank">
        Peargent
      </a>
      .
    </span>
  </Footer>
)

export default async function DocsLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" dir="ltr" suppressHydrationWarning>
      <Head />
      <body>
        <Layout
          navbar={navbar}
          pageMap={await getPageMap('/docs')}
          docsRepositoryBase="https://github.com/yourusername/peargent/tree/main/docs"
          footer={footer}
        >
          {children}
        </Layout>
      </body>
    </html>
  )
}
