#!/usr/bin/make -f

PACKAGES = -package http -package cryptokit

%.cmx: %.ml
	ocamlfind ocamlopt $(PACKAGES) -I ../lib -o $@ -c $<

pad: pad.cmx
	ocamlfind ocamlopt $(PACKAGES) -I ../lib -o $@ -linkpkg $^

clean:
	rm --force trading *.cmi *.cmo *.cmx
