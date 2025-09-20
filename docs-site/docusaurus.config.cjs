/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Nexla Python SDK',
  tagline: 'Python SDK for Nexla Data Operations',
  url: process.env.SITE_URL || 'http://localhost:3001',
  baseUrl: '/',
  organizationName: 'Nexla',
  projectName: 'Nexla Python SDK',
  favicon: '/img/favicon.ico',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en']
  },
  themes: ['@docusaurus/theme-mermaid'],
  markdown: {
    mermaid: true
  },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.cjs'),
          editUrl: process.env.DOCS_EDIT_URL || undefined,
          routeBasePath: '/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true
        },
        blog: false,
        theme: {
          customCss: undefined
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
          filename: 'sitemap.xml'
        }
      })
    ]
  ],
  plugins: [
    // Local search fallback when Algolia env vars are missing
    !Boolean(process.env.ALGOLIA_APP_ID && process.env.ALGOLIA_API_KEY && process.env.ALGOLIA_INDEX_NAME) && [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        docsRouteBasePath: '/',
        indexDocs: true,
        indexBlog: false
      }
    ]
  ].filter(Boolean),
  themeConfig: {
    navbar: {
      title: 'Nexla SDK',
      logo: {
        alt: 'Nexla Logo',
        src: '/img/logo.svg'
      },
      items: [
        {to: '/', label: 'Docs', position: 'left'},
        {to: '/api/python/overview', label: 'API', position: 'left'},
        {
          href: 'https://github.com/nexla-opensource/nexla-sdk',
          label: 'GitHub',
          position: 'right'
        },
        {
          type: 'docsVersionDropdown',
          position: 'right'
        }
      ]
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: 'Getting Started', to: '/getting-started'},
            {label: 'API Reference', to: '/api/python/overview'}
          ]
        },
        {
          title: 'Community',
          items: [
            {label: 'GitHub', href: 'https://github.com/nexla-opensource/nexla-sdk'}
          ]
        }
      ],
      copyright: `© ${new Date().getFullYear()} Nexla.`
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true
    },
    prism: {
      additionalLanguages: ['bash', 'json', 'python']
    },
    // Algolia primary search is auto-enabled when env vars are present
    algolia: Boolean(process.env.ALGOLIA_APP_ID && process.env.ALGOLIA_API_KEY && process.env.ALGOLIA_INDEX_NAME)
      ? {
          appId: process.env.ALGOLIA_APP_ID,
          apiKey: process.env.ALGOLIA_API_KEY,
          indexName: process.env.ALGOLIA_INDEX_NAME,
          contextualSearch: true
        }
      : undefined,
    metadata: [
      {name: 'og:title', content: 'Nexla Python SDK'},
      {name: 'og:type', content: 'website'},
      {name: 'twitter:card', content: 'summary_large_image'},
      {name: 'twitter:title', content: 'Nexla Python SDK'}
    ]
  },
  headTags: [
    {
      tagName: 'link',
      attributes: {rel: 'canonical', href: process.env.SITE_URL || 'http://localhost:3001'}
    },
    {
      tagName: 'script',
      attributes: {type: 'application/ld+json'},
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: 'Nexla Python SDK',
        url: process.env.SITE_URL || 'http://localhost:3001',
        potentialAction: {
          '@type': 'SearchAction',
          target: `${process.env.SITE_URL || 'http://localhost:3001'}/?q={search_term_string}`,
          'query-input': 'required name=search_term_string'
        }
      })
    },
    {
      tagName: 'script',
      attributes: {type: 'application/ld+json'},
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'SoftwareApplication',
        name: 'Nexla Python SDK',
        applicationCategory: 'DeveloperApplication',
        operatingSystem: 'Any',
        url: process.env.SITE_URL || 'http://localhost:3001'
      })
    }
  ]
};

module.exports = config;