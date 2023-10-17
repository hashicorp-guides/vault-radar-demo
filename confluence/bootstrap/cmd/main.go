// Copyright (c) HashiCorp, Inc.
<<<<<<< Updated upstream
=======
// SPDX-License-Identifier: MPL-2.0
>>>>>>> Stashed changes

package main

import (
	"bytes"
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"os"
	"strings"

	"github.com/brianvoe/gofakeit/v6"
	retryablehttp "github.com/hashicorp/go-retryablehttp"
	"gopkg.in/yaml.v3"
)

const (
	confluenceInstanceURL = "http://localhost:8090"
	spaceName             = "Vault Radar Demo"
	spaceKey              = "VRD"
	spaceDescription      = "A Confluence Space for demoing and/or testing vault-radar"
	numberOfPagesToCreate = 50
	// we will randomly choose between 1 and maxNumberOfVersionsToCreate for each page and create that many different
	// versions of the page
	maxNumberOfVersionsToCreate = 10
	// this controls how frequent secrets are sprinkled in with the normal page contents.
	// 1 / secretSprinkleRatio = % chance a secret will be included in a generated page
	secretSprinkleRatio = 3

	// Confluence Cloud Authentication
	atlassianAPIToken = "" // Confluence Cloud Only
	atlassianEmail    = "" // Confluence Cloud Only
	// Confluence Server Authentication
	personalAccessToken = "" // Confluence Server v7.9+ only
	userName            = "" // Confluence Server only
	password            = "" // Confluence Server

	sampleSecretsPath = "../../secrets.yaml"
)

// restClient is the http client used to communicate with the confluence instance
var restClient *http.Client

func main() {
	ctx := context.Background()

	if spaceExistsAlready(ctx) {
		fmt.Printf("Found a space with key: %s\n", spaceKey)
	} else {
		createSpace(ctx)
	}

	sp := NewSecretProvider()

	fmt.Printf("Creating %d pages\n", numberOfPagesToCreate)

	// create pages with different versions
	for i := 0; i < numberOfPagesToCreate; i++ {
		pageID := createPage(ctx, &sp)
		versionCount := rand.Intn(maxNumberOfVersionsToCreate)
		for v := 2; v <= versionCount; v++ {
			updatePage(ctx, pageID, v, &sp)
		}
	}

	fmt.Println("bootstrapping complete")
}

// pageRequestBody is a struct representing a json blob for a confluence page in a request or response
type pageRequestBody struct {
	Type    string    `json:"type,omitempty"`
	Title   string    `json:"title,omitempty" fake:"{sentence:4}"`
	Space   *space    `json:"space,omitempty"`
	Version *version  `json:"version,omitempty" fake:"skip"`
	Body    *pageBody `json:"body,omitempty"`
}

// space is a struct representing a space json blob in a confluence request/response
type space struct {
	Key string `json:"key,omitempty"`
}

// pageBody is a struct representing a body json blob in a confluence page request/response
type pageBody struct {
	Storage *storage `json:"storage,omitempty"`
}

// storage is a struct representing a storage json blob in a confluence request/response
type storage struct {
	Value          string `json:"value,omitempty"`
	Representation string `json:"representation,omitempty"`
}

// version is a struct representing a version json blob in a confluence request/response
type version struct {
	Number int `json:"number,omitempty"`
}

// secretProvider round robins through a list of secrets providing one each time Get is called
type secretProvider struct {
	secretPool []interface{}
	index      int
}

// NewSecretProvider initializes and constructs a secret provider using the default secret sample sources
func NewSecretProvider() secretProvider {
	return secretProvider{
		secretPool: getSecretSamples(),
		index:      0,
	}
}

// Get returns the next secret from the sample pool
func (p *secretProvider) Get() interface{} {
	res := p.secretPool[p.index]
	if p.index+1 == len(p.secretPool) {
		p.index = 0
	} else {
		p.index = p.index + 1
	}
	return res
}

// getSecretSamples reads the secrets in from a file into a slice
func getSecretSamples() []interface{} {
	// read in sample scanning targets
	b, err := os.ReadFile(sampleSecretsPath)
	if err != nil {
		fmt.Printf("error reading sample secrets: %s\n", err)
		os.Exit(1)
	}

	sampleMap := struct {
		Samples map[string][]interface{} `yaml:"samples"`
	}{}
	err = yaml.Unmarshal(b, &sampleMap)
	if err != nil {
		fmt.Printf("error unmarshaling sample secrets: %s\n", err)
		os.Exit(1)
	}

	secretSamples := []interface{}{}
	for _, samples := range sampleMap.Samples {
		secretSamples = append(secretSamples, samples...)
	}

	return secretSamples
}

// getClient returns a configured http client, reusing one if
func getClient() *http.Client {
	if restClient != nil {
		return restClient
	}

	rhc := retryablehttp.NewClient()
	rhc.Logger = nil
	restClient = rhc.StandardClient()

	return restClient
}

// spaceExistsAlready fetches the space, and returns false if makes and executes the request to create a Confluence space
func spaceExistsAlready(ctx context.Context) bool {
	url := confluenceInstanceURL
	if isCloud() {
		url = url + "/wiki"
	}

	url = url + "/rest/api/space/" + spaceKey

	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		fmt.Printf("error building request to fetch a space: %s\n", err)
		os.Exit(1)
	}
	setHeaders(req)

	resp, err := getClient().Do(req)
	if err != nil {
		fmt.Printf("error making request to fetch %s space: %s\n", spaceKey, err)
		os.Exit(1)
	}

	if resp.StatusCode == 200 || resp.StatusCode == 404 {
		// 404 is expected when the space is not created yet
		return resp.StatusCode == 200
	}

	// likely there's an error
	checkResponse(resp)
	return false
}

// createSpace makes and executes the request to create a Confluence space
func createSpace(ctx context.Context) {
	url := confluenceInstanceURL
	if isCloud() {
		url = url + "/wiki"
	}

	url = url + "/rest/api/space"

	body := struct {
		Key  string `json:"key"`
		Name string `json:"name"`
	}{
		Key:  spaceKey,
		Name: spaceName,
	}

	bb := new(bytes.Buffer)
	err := json.NewEncoder(bb).Encode(body)
	if err != nil {
		fmt.Printf("error encoding create space body: %s\n", err)
		os.Exit(1)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bb)
	if err != nil {
		fmt.Printf("error building request to create a space: %s\n", err)
		os.Exit(1)
	}

	setHeaders(req)

	fmt.Printf("Creating Space: %s - %s\n", spaceName, spaceKey)
	_, err = getClient().Do(req)
	if err != nil {
		fmt.Printf("error making request to create a space: %s\n", err)
		fmt.Println("continuing in case the error is the space already exists, which happens when re-running the script")
	}
}

func createPage(ctx context.Context, secretProvider *secretProvider) string {
	var secret interface{}
	r := rand.Intn(secretSprinkleRatio)
	if r == 0 {
		secret = secretProvider.Get()
	}

	var secretVal string
	switch val := secret.(type) {
	case string:
		secretVal = val
	case map[string]interface{}:
		for k, v := range val {
			secretVal += fmt.Sprintf("%s = %#v\n", k, v)
		}
	}

	var body pageRequestBody
	gofakeit.Struct(&body)
	body.Type = "page"
	body.Space.Key = spaceKey
	body.Body.Storage.Representation = "storage"
	body.Body.Storage.Value = fmt.Sprintf(`<p>%s<br/><br/>%s<br/><br/>%s</p>`,
		gofakeit.LoremIpsumParagraph(1, 10, 15, ""),
		gofakeit.LoremIpsumParagraph(1, 10, 15, ""),
		secretVal)

	bb := new(bytes.Buffer)
	err := json.NewEncoder(bb).Encode(body)
	if err != nil {
		fmt.Printf("error encoding create page body: %s\n", err)
		os.Exit(1)
	}

	url := confluenceInstanceURL
	if isCloud() {
		url = url + "/wiki"
	}
	url = url + "/rest/api/content"

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, url, bb)
	if err != nil {
		fmt.Printf("error building request to create a page: %s\n", err)
		os.Exit(1)
	}

	setHeaders(req)

	resp, err := getClient().Do(req)
	if err != nil {
		fmt.Printf("error making request to create a page: %s\n", err)
		os.Exit(1)
	}
	checkResponse(resp)

	// Get pageID
	respBody := struct {
		ID string `json:"id"`
	}{}

	err = json.NewDecoder(resp.Body).Decode(&respBody)
	if err != nil {
		fmt.Print("error reading get first page response body: %w", err)
		os.Exit(1)
	}

	return respBody.ID
}

// updatePage constructs and executes a request to update a page similar to how it's created
func updatePage(ctx context.Context, pageID string, v int, secretProvider *secretProvider) {
	url := confluenceInstanceURL
	if isCloud() {
		url = url + "/wiki"
	}
	url = url + "/rest/api/content/" + pageID

	var secret string
	r := rand.Intn(secretSprinkleRatio)
	if r == 0 {
		// sprinkle secrets into the versions, except for the last version
		secret = fmt.Sprintf("%v\n", secretProvider.Get())
	}

	pageContent := fmt.Sprintf(`<p>%s<br/><br/>%s<br/><br/>%s</p>`,
		gofakeit.LoremIpsumParagraph(1, 10, 15, ""),
		gofakeit.LoremIpsumParagraph(1, 10, 15, ""),
		secret)

	updatePageBody := pageRequestBody{
		Title:   gofakeit.Sentence(4),
		Type:    "page",
		Version: &version{Number: v},
		Body: &pageBody{
			Storage: &storage{
				Representation: "storage",
				Value:          pageContent,
			},
		},
	}

	bb := new(bytes.Buffer)
	err := json.NewEncoder(bb).Encode(updatePageBody)
	if err != nil {
		fmt.Printf("error encoding update page body: %s\n", err)
		os.Exit(1)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPut, url, bb)
	if err != nil {
		fmt.Printf("error building request to update first page again: %s\n", err)
		os.Exit(1)
	}
	setHeaders(req)

	resp, err := getClient().Do(req)
	if err != nil {
		fmt.Printf("error making request to update first page again: %s\n", err)
		os.Exit(1)
	}
	checkResponse(resp)
}

// setHeaders sets the common required headers to complete a request the confluence server
func setHeaders(req *http.Request) {
	req.Header.Add("X-Atlassian-Token", "no-check")
	req.Header.Add("Content-Type", "application/json")
	setAuthHeader(req)
}

// setAuthHeader sets the appropriate header and value depending on the available credentials
func setAuthHeader(req *http.Request) {
	if isCloud() {
		req.Header.Add("Authorization",
			fmt.Sprintf("Basic %s", base64.StdEncoding.EncodeToString([]byte(atlassianEmail+":"+atlassianAPIToken))))
	} else {
		if personalAccessToken != "" {
			req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", personalAccessToken))
		} else {
			req.Header.Add("Authorization",
				fmt.Sprintf("Basic %s", base64.StdEncoding.EncodeToString([]byte(userName+":"+password))))
		}
	}
}

// checkResponse checks for unsuccessful response codes and attempts to read the response body for debugging
func checkResponse(resp *http.Response) {
	if resp.StatusCode != 200 {
		defer resp.Body.Close()
		b, err := io.ReadAll(resp.Body)
		if err != nil {
			fmt.Printf("response returned %d, tried to read the body but received error: %s", resp.StatusCode, err)
			os.Exit(1)
		}
		fmt.Printf("response returned %d, with body: %s ", resp.StatusCode, string(b))
		os.Exit(1)
	}
}

// isCloud returns true when cloud creds are set
func isCloud() bool {
	return strings.Contains(confluenceInstanceURL, "atlassian.net")
}
