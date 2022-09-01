dev-env:
	kind create cluster
	kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
	kubectl -n tekton-pipelines patch configmaps feature-flags --patch '{"data": {"enable-tekton-oci-bundles": "true"}}'
	kubectl apply -k tekton

venv:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

build-image:
	podman build -t quay.io/bpimente/cachi2:poc .
	podman push quay.io/bpimente/cachi2:poc

tekton-bundle:
	tkn bundle push quay.io/bpimente/cachi2:task-bundle -f tekton/task.yaml
