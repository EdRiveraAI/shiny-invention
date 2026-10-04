# How to Build a Plugin You Can Sell

A step-by-step guide from idea to first paying customer.

"Plugin" means different things on different platforms, and the platform you pick decides how
you get paid, how you ship updates, and who your buyers are. This guide gives you:

1. A platform decision table (Step 1)
2. A full worked example: a **paid WordPress plugin**, the most mature market for selling
   plugins, with licensing, payments, and automatic updates (Steps 2–9)
3. Notes on how the same process changes for Shopify, Chrome, Figma, and Claude Code/MCP plugins
   (Step 10)

> Prices, fees, and marketplace rules change often. Check each platform's current terms before
> you commit to one.

---

## Step 1 — Pick the platform and the problem

### Choose a platform

| Platform | Who buys | How you get paid | Difficulty | Notes |
|---|---|---|---|---|
| **WordPress** (PHP) | Site owners, agencies, freelancers | Your own store (Freemius, Lemon Squeezy, Easy Digital Downloads), or CodeCanyon | Medium | Huge market (~40% of the web). Free version on WordPress.org works as a marketing funnel. |
| **Shopify app** (JS/TS, Remix/React) | Store owners | Shopify Billing API (required for App Store apps) — monthly subscriptions | High | Merchants are used to paying monthly. Strict review process. |
| **Chrome extension** (JS) | Everyone | Your own Stripe/ExtPay integration — the Chrome Web Store no longer handles payments | Low–Medium | Easy to build, harder to monetize; consumers are price-sensitive. |
| **Figma plugin** (JS/TS) | Designers | Figma Community paid plugins (seller approval needed) or your own licensing | Low–Medium | Smaller market, but buyers value time savings. |
| **Claude Code plugin / MCP server** | Developers, teams using AI | No built-in store — charge for a hosted backend/API key the plugin calls | Medium | New and growing; you sell the service, not the files. |
| **Desktop apps** (VS Code, Obsidian, Adobe, DAWs/VST audio) | Varies | Mostly your own licensing | Varies | Audio plugins (VST/AU) are a strong paid niche if you know C++/JUCE. |

**Rule of thumb:** pick the platform you (a) already know, and (b) whose users you understand.
Understanding the buyer matters more than the tech.

### Find a problem worth paying for

Plugins sell when they **save time, make money, or prevent loss** for a business. Ways to find one:

- Read 1–3 star reviews of popular plugins in your platform's directory. Every repeated complaint
  is a product idea.
- Search support forums, Reddit, and Facebook groups for "is there a plugin that…".
- Look at what you or your clients already pay a developer to do by hand.
- Check that competitors exist and charge money — that proves demand. No competitors usually
  means no market, not a gold mine.

**Validate before building:** write a one-page landing page describing the plugin, a price, and an
"Get early access" email form. Share it where your buyers hang out. If you can't get ~20–50
signups, rethink the idea before writing code.

---

## Step 2 — Plan the product and business model

Decide these up front, because they shape the code:

| Decision | Common choice | Why |
|---|---|---|
| **Model** | Freemium: free version + paid "Pro" | Free version gets distribution; Pro gets revenue. |
| **Pricing** | Annual license by number of sites, e.g. 1 site $49/yr · 5 sites $99/yr · unlimited $199/yr | Recurring revenue funds updates and support. |
| **What's Pro** | Features businesses need: automation, integrations, advanced reports, priority support | Keep the free version genuinely useful, or nobody installs it. |
| **License enforcement** | License key that unlocks **updates and support** | Keys are easy to share; updates and support are what customers really pay for. |

> **GPL note (WordPress):** WordPress plugins inherit the GPL license. Buyers can legally
> redistribute your code. That's normal and fine — your paying customers are paying for
> **automatic updates, support, and trust**, not for the files. Don't waste time on heavy DRM.

Write a short spec: the 3–5 core features of v1.0, which are free vs. Pro, and what you will
**not** build yet. Ship small.

---

## Step 3 — Set up your development environment

For WordPress:

1. Install a local WordPress: [LocalWP](https://localwp.com/) (easiest), `wp-env` (Docker,
   `npm i -g @wordpress/env && wp-env start`), or DDEV.
2. Install tools:
   - PHP 8.x and [Composer](https://getcomposer.org/)
   - [WP-CLI](https://wp-cli.org/)
   - Git + a private GitHub repository (the Pro code should stay private)
   - Code standards: `composer require --dev wp-coding-standards/wpcs dealerdirect/phpcodesniffer-composer-installer`
3. Turn on debugging in `wp-config.php`:

```php
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
```

---

## Step 4 — Build the plugin

### Folder structure

```
my-awesome-plugin/
├── my-awesome-plugin.php      # Main file with the plugin header
├── uninstall.php              # Cleans up options when the plugin is deleted
├── readme.txt                 # Required for WordPress.org
├── includes/
│   ├── class-plugin.php       # Bootstraps everything
│   ├── class-settings.php     # Admin settings page
│   └── class-license.php      # License activation + checks (Pro only)
├── assets/
│   ├── css/
│   └── js/
└── languages/                 # Translation files
```

### Main plugin file

```php
<?php
/**
 * Plugin Name:       My Awesome Plugin
 * Plugin URI:        https://example.com/my-awesome-plugin
 * Description:       Short, benefit-focused description.
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            Your Name
 * Author URI:        https://example.com
 * License:           GPL-2.0-or-later
 * Text Domain:       my-awesome-plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Block direct access.
}

define( 'MAP_VERSION', '1.0.0' );
define( 'MAP_FILE', __FILE__ );
define( 'MAP_DIR', plugin_dir_path( __FILE__ ) );

require_once MAP_DIR . 'includes/class-plugin.php';

register_activation_hook( __FILE__, array( 'MAP_Plugin', 'activate' ) );
register_deactivation_hook( __FILE__, array( 'MAP_Plugin', 'deactivate' ) );

add_action( 'plugins_loaded', array( 'MAP_Plugin', 'instance' ) );
```

### Bootstrap class

```php
<?php
// includes/class-plugin.php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

final class MAP_Plugin {
	private static $instance = null;

	public static function instance() {
		if ( null === self::$instance ) {
			self::$instance = new self();
		}
		return self::$instance;
	}

	private function __construct() {
		require_once MAP_DIR . 'includes/class-settings.php';
		new MAP_Settings();

		if ( file_exists( MAP_DIR . 'includes/class-license.php' ) ) {
			require_once MAP_DIR . 'includes/class-license.php';
			new MAP_License();
		}
	}

	public static function activate() {
		add_option( 'map_settings', array( 'enabled' => true ) );
	}

	public static function deactivate() {
		wp_clear_scheduled_hook( 'map_daily_license_check' );
	}

	/** Use this everywhere you gate a Pro feature. */
	public static function is_pro() {
		return 'valid' === get_option( 'map_license_status' );
	}
}
```

### Settings page (with the security basics done right)

```php
<?php
// includes/class-settings.php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class MAP_Settings {
	public function __construct() {
		add_action( 'admin_menu', array( $this, 'add_menu' ) );
		add_action( 'admin_init', array( $this, 'register' ) );
	}

	public function add_menu() {
		add_options_page(
			__( 'My Awesome Plugin', 'my-awesome-plugin' ),
			__( 'My Awesome Plugin', 'my-awesome-plugin' ),
			'manage_options',                 // Capability check.
			'my-awesome-plugin',
			array( $this, 'render' )
		);
	}

	public function register() {
		register_setting( 'map_settings_group', 'map_settings', array(
			'sanitize_callback' => array( $this, 'sanitize' ), // Sanitize input.
		) );
	}

	public function sanitize( $input ) {
		return array(
			'enabled' => ! empty( $input['enabled'] ),
			'label'   => sanitize_text_field( $input['label'] ?? '' ),
		);
	}

	public function render() {
		if ( ! current_user_can( 'manage_options' ) ) {
			return;
		}
		$opts = get_option( 'map_settings', array() );
		?>
		<div class="wrap">
			<h1><?php esc_html_e( 'My Awesome Plugin', 'my-awesome-plugin' ); ?></h1>
			<form method="post" action="options.php">
				<?php settings_fields( 'map_settings_group' ); // Adds the nonce. ?>
				<label>
					<input type="checkbox" name="map_settings[enabled]" value="1" <?php checked( ! empty( $opts['enabled'] ) ); ?> />
					<?php esc_html_e( 'Enable', 'my-awesome-plugin' ); ?>
				</label>
				<p>
					<input type="text" name="map_settings[label]" value="<?php echo esc_attr( $opts['label'] ?? '' ); ?>" />
				</p>
				<?php if ( MAP_Plugin::is_pro() ) : ?>
					<!-- Pro-only settings go here. -->
				<?php else : ?>
					<p><a href="https://example.com/pricing" target="_blank"><?php esc_html_e( 'Upgrade to Pro', 'my-awesome-plugin' ); ?></a></p>
				<?php endif; ?>
				<?php submit_button(); ?>
			</form>
		</div>
		<?php
	}
}
```

### Security checklist (reviewers and buyers will check this)

- **Sanitize every input:** `sanitize_text_field()`, `absint()`, `sanitize_email()`, `esc_url_raw()`
- **Escape every output:** `esc_html()`, `esc_attr()`, `esc_url()`, `wp_kses_post()`
- **Nonces on every form and AJAX call:** `wp_nonce_field()` / `check_admin_referer()` / `check_ajax_referer()`
- **Capability checks:** `current_user_can( 'manage_options' )` before any admin action
- **Database:** always `$wpdb->prepare()` for queries with variables
- **Prefix everything** (`map_`, `MAP_`) so you don't collide with other plugins
- **Clean uninstall:** delete your options in `uninstall.php`

```php
<?php
// uninstall.php
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}
delete_option( 'map_settings' );
delete_option( 'map_license_key' );
delete_option( 'map_license_status' );
```

---

## Step 5 — Add licensing and payments

You need three things: **a checkout**, **license keys**, and **update delivery**. Don't build
these from scratch. Pick one:

| Option | What it handles | Good for |
|---|---|---|
| **Freemius** | Checkout, licenses, updates, analytics, free→Pro upgrade inside WP admin, sales tax | Fastest path for WordPress specifically. Takes a revenue share. |
| **Lemon Squeezy** or **Paddle** | Checkout, subscriptions, license keys, global sales tax/VAT as *merchant of record* | Any platform. You handle update delivery yourself. |
| **Easy Digital Downloads + Software Licensing add-on** | Self-hosted store, licenses, updates on your own WordPress site | Full control, no revenue share, more maintenance. |
| **Gumroad** | Simple checkout + license keys | Quick start; fewer subscription/team features. |
| **CodeCanyon (Envato)** | Marketplace with built-in audience and payments | Discovery without marketing; large revenue share and price pressure. |

> **Merchant of record** (Lemon Squeezy, Paddle, Freemius) means *they* are legally the seller and
> collect and remit VAT/sales tax worldwide. That saves you a large tax headache early on.

### Example: license activation with Lemon Squeezy's license API

```php
<?php
// includes/class-license.php
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class MAP_License {
	const API = 'https://api.lemonsqueezy.com/v1/licenses/';

	public function __construct() {
		add_action( 'admin_post_map_activate_license', array( $this, 'handle_activate' ) );
		add_action( 'map_daily_license_check', array( $this, 'validate' ) );
		if ( ! wp_next_scheduled( 'map_daily_license_check' ) ) {
			wp_schedule_event( time(), 'daily', 'map_daily_license_check' );
		}
	}

	public function handle_activate() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( 'Not allowed' );
		}
		check_admin_referer( 'map_activate_license' );

		$key  = sanitize_text_field( wp_unslash( $_POST['license_key'] ?? '' ) );
		$resp = wp_remote_post( self::API . 'activate', array(
			'timeout' => 15,
			'headers' => array( 'Accept' => 'application/json' ),
			'body'    => array(
				'license_key'   => $key,
				'instance_name' => home_url(),
			),
		) );

		$data = is_wp_error( $resp ) ? null : json_decode( wp_remote_retrieve_body( $resp ), true );

		if ( ! empty( $data['activated'] ) ) {
			update_option( 'map_license_key', $key );
			update_option( 'map_license_instance', $data['instance']['id'] );
			update_option( 'map_license_status', 'valid' );
		} else {
			update_option( 'map_license_status', 'invalid' );
		}

		wp_safe_redirect( admin_url( 'options-general.php?page=my-awesome-plugin' ) );
		exit;
	}

	/** Re-checks the key daily so expired or refunded licenses stop getting Pro features. */
	public function validate() {
		$key = get_option( 'map_license_key' );
		if ( ! $key ) {
			return;
		}
		$resp = wp_remote_post( self::API . 'validate', array(
			'timeout' => 15,
			'headers' => array( 'Accept' => 'application/json' ),
			'body'    => array(
				'license_key' => $key,
				'instance_id' => get_option( 'map_license_instance' ),
			),
		) );
		if ( is_wp_error( $resp ) ) {
			return; // Network error: keep the last known status rather than locking the customer out.
		}
		$data = json_decode( wp_remote_retrieve_body( $resp ), true );
		update_option( 'map_license_status', ! empty( $data['valid'] ) ? 'valid' : 'invalid' );
	}
}
```

Add a matching form to your settings page:

```php
<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
	<?php wp_nonce_field( 'map_activate_license' ); ?>
	<input type="hidden" name="action" value="map_activate_license" />
	<input type="text" name="license_key" placeholder="License key" />
	<?php submit_button( __( 'Activate', 'my-awesome-plugin' ) ); ?>
</form>
```

Also add **Deactivate** (calls `/v1/licenses/deactivate`) so customers can move a license to a new
site without emailing you.

---

## Step 6 — Ship automatic updates to paying customers

WordPress.org only updates plugins it hosts, so your Pro plugin needs its own update channel:

- **Freemius / EDD Software Licensing:** built in — include their SDK/updater class.
- **Lemon Squeezy / Paddle / Gumroad:** use the open-source
  [plugin-update-checker](https://github.com/YahnisElsts/plugin-update-checker) library and host a
  small JSON file (version, download URL, changelog) on your server. Have your download endpoint
  check the license key before serving the zip.

```php
require MAP_DIR . 'vendor/yahnis-elsts/plugin-update-checker/load-v5.php';

$checker = YahnisElsts\PluginUpdateChecker\v5\PucFactory::buildUpdateChecker(
	'https://updates.example.com/my-awesome-plugin.json',
	MAP_FILE,
	'my-awesome-plugin'
);
$checker->addQueryArgFilter( function ( $args ) {
	$args['license_key'] = get_option( 'map_license_key' );
	return $args;
} );
```

---

## Step 7 — Test like a customer

- [ ] Test on the minimum and latest WordPress and PHP versions you claim to support
- [ ] Test with popular themes and plugins active (WooCommerce, Elementor, Yoast, a caching plugin)
- [ ] Test on multisite if you claim support
- [ ] Run the official **Plugin Check** plugin and `phpcs --standard=WordPress`
- [ ] Fresh install → activate → configure → deactivate → delete: no errors, no leftover data
- [ ] License flows: activate, invalid key, expired key, deactivate, move to a new site
- [ ] Upgrade path: install v1.0.0, then update to v1.0.1 through your update channel
- [ ] Get 5–10 beta users (from your Step 1 email list) to use it for a week before launch

---

## Step 8 — Package and launch

### Build the release zip

```bash
# Exclude dev files from the customer zip
zip -r my-awesome-plugin-1.0.0.zip my-awesome-plugin \
  -x "*/.git/*" "*/node_modules/*" "*/tests/*" "*/.github/*" "*/composer.lock" "*/phpcs.xml"
```

Automate this with a GitHub Action that builds and uploads the zip whenever you push a version tag.

### Free version on WordPress.org (your marketing funnel)

1. Write `readme.txt` in the [WordPress.org readme format](https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/)
   — benefit-focused description, screenshots, FAQ, changelog.
2. Submit at <https://wordpress.org/plugins/developers/add/>. Review can take days to weeks.
3. Rules to know: the free version must be fully functional on its own (no locked "trialware"
   features), no tracking without opt-in, and upsell notices must be dismissible and limited.
4. Once approved you get an SVN repository — commit your code there to publish updates.

### Sales site

You need, at minimum:

- **Landing page:** headline that states the outcome, a demo GIF/video, features, pricing table,
  FAQ, testimonials from beta users
- **Checkout** from your payment provider
- **Documentation** (setup guide + common questions) — good docs cut support load dramatically
- **Legal pages:** Terms of Service, refund policy (14–30 days is standard), privacy policy
- **Support channel:** help desk or a support email with a stated response time

---

## Step 9 — Market, support, and grow

**Getting customers**

- WordPress.org free version → in-plugin "Upgrade to Pro" links → your pricing page
- SEO content on your site: "how to [problem your plugin solves] in WordPress" tutorials
- YouTube walkthroughs; ask WordPress YouTubers to review it (give them a free license)
- Communities: WordPress Facebook groups, r/Wordpress, Post Status, agency Slack groups
- Launch discounts for your early-access list; launch on Product Hunt
- Lifetime deal sites (AppSumo) can bring fast cash and users, but price carefully — lifetime
  customers still cost you support forever

**Running it as a business**

- Reply to support quickly — reviews and renewals depend on it
- Ship small updates regularly and publish a changelog; active updates drive renewals
- Track: free installs, free→Pro conversion (1–3% is typical), renewal rate, refunds, churn
- Raise prices as you add value; grandfather existing customers
- Register a business entity (e.g. an LLC) and keep plugin income in a separate bank account;
  talk to an accountant about taxes in your country

---

## Step 10 — If you choose a different platform

The steps above stay the same (validate → plan → build → license → test → launch → market). What
changes:

### Shopify app
- Scaffold with `shopify app init` (Shopify CLI); the default template is Remix/React + Node.
- Apps in the Shopify App Store **must** bill through the Shopify Billing API (recurring
  subscriptions, usage charges). Shopify takes a revenue share above a lifetime revenue threshold —
  check the current partner terms.
- Expect a strict review: performance, GDPR webhooks, Polaris UI conventions, clear onboarding.

### Chrome extension
- Manifest V3 (`manifest.json`, service worker, content scripts).
- The Chrome Web Store doesn't process payments anymore: use ExtPay, or Stripe Checkout plus your
  own backend that verifies the user's subscription.
- Put valuable logic on your server — anything in the extension can be read by the user.

### Figma plugin
- Create via Figma → Plugins → Development → New plugin; code in TypeScript with `figma.*` APIs.
- Apply to sell through the Figma Community, or use your own license-key check.

### Claude Code plugin / MCP server
- A Claude Code plugin is a folder with `.claude-plugin/plugin.json` that can bundle skills,
  slash commands, agents, hooks, and MCP servers. You distribute it through a marketplace (a git
  repo with `.claude-plugin/marketplace.json`); users install it with
  `/plugin marketplace add <owner>/<repo>` and `/plugin install`.
- There's no built-in payment, and the plugin files themselves are readable. The way to charge is
  to **sell access to a hosted service**: your plugin ships an MCP server (or calls your API) that
  requires an API key, and customers buy the key through Stripe/Lemon Squeezy/Paddle. The free
  plugin is the funnel; the paid API is the product.
- See the Claude Code docs on plugins and the MCP specification for current details.

---

## Quick-start checklist

- [ ] Pick a platform you know and a buyer you understand
- [ ] Find a painful, recurring problem; confirm competitors charge for it
- [ ] Validate with a landing page + email signups
- [ ] Define v1.0 scope and free vs. Pro split; set prices
- [ ] Set up local dev environment and coding standards
- [ ] Build the core features securely (sanitize, escape, nonces, capability checks)
- [ ] Add licensing + checkout (Freemius / Lemon Squeezy / Paddle / EDD)
- [ ] Add an update channel for paying customers
- [ ] Test across versions, themes, plugins, and license states; run a beta
- [ ] Publish the free version, launch the sales site with docs and legal pages
- [ ] Market consistently, support quickly, update regularly
