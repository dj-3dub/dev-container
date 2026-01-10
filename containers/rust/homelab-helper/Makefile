.PHONY: build run check fmt lint

build:
	cargo build --release

run:
	cargo run -- check 192.168.2.51

check:
	cargo check

fmt:
	cargo fmt

lint:
	cargo clippy -- -D warnings
