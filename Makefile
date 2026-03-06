wg-create:
	rm -f gateway.conf
	FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) flyctl wireguard create personal fra gateway gateway.conf

wg-list:
	FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) flyctl wireguard list

gateway:
	docker compose up --build gateway

wg-remove-all:
	@export FLY_API_TOKEN=$$(cat flyio_token_gateway.txt) && \
	org=$$(flyctl status -j | jq -r '.Organization.Slug') && \
	for name in $$(flyctl wireguard list -j | jq -r '.[].Name'); do \
		flyctl wireguard remove $$org $$name; \
	done