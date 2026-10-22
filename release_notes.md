# Release notes

- Add Nette Framework detection from the `X-Powered-By: Nette Framework` prefix, independent of version.
- Add ReactPHP HTTP server detection from the `Server: ReactPHP/` prefix; does not identify EventLoop-only usage or servers hiding this header.
- Add Laravel detection from the `laravel_session` HTTP cookie.
- Add MISP detection from HTTP cookie names prefixed with `misp-`.
- Add Ivanti Connect Secure detection from HTTP titles.
- Add FRITZ!Repeater detection.
- Add Danfoss StoreView detection.
- Extend Reolink detection.
- Add Home Assistant detection.
- Extend OpenVPN detection.
- Tag Nginx default installation pages.
- Split SonicWall firewall and SMA detection.
- Add Passbolt detection.
- Add One Identity Safeguard detection.
