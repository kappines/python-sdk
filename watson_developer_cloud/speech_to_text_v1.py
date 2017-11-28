# Copyright 2016 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
The v1 Speech to Text service
(https://www.ibm.com/watson/developercloud/speech-to-text.html)
"""

from .watson_service import WatsonService
import json


class SpeechToTextV1(WatsonService):
    default_url = "https://stream.watsonplatform.net/speech-to-text/api"

    def __init__(self, url=default_url, **kwargs):
        WatsonService.__init__(self, 'speech_to_text', url, **kwargs)

    #########################
    # sessionless
    #########################

    def recognize(self, audio, content_type, continuous=None, model=None,
                  customization_id=None,
                  inactivity_timeout=None,
                  keywords=None, keywords_threshold=None,
                  max_alternatives=None,
                  word_alternatives_threshold=None,
                  word_confidence=None, timestamps=None, interim_results=None,
                  profanity_filter=None,
                  smart_formatting=None,
                  speaker_labels=None,
                  customization_weight=None):
        """
        Returns the recognized text from the audio input
        """
        headers = {'content-type': content_type}
        params = {'continuous': continuous,
                  'inactivity_timeout': inactivity_timeout,
                  'keywords': keywords,
                  'keywords_threshold': keywords_threshold,
                  'max_alternatives': max_alternatives,
                  'model': model,
                  'customization_id': customization_id,
                  'word_alternatives_threshold': word_alternatives_threshold,
                  'word_confidence': word_confidence,
                  'timestamps': timestamps,
                  'interim_results': interim_results,
                  'profanity_filter': profanity_filter,
                  'smart_formatting': smart_formatting,
                  'speaker_labels': speaker_labels,
                  'customization_weight': customization_weight}

        return self.request(method='POST', url='/v1/recognize',
                            headers=headers,
                            data=audio, params=params,
                            stream=True, accept_json=True)

    #########################
    # models
    #########################

    def models(self):
        """
        Returns the list of available models to use with recognize
        """
        return self.request(method='GET', url='/v1/models', accept_json=True)

    def get_model(self, model_id):
        """
        :param model_id: The identifier of the desired model
        :return: A single instance of a Model object with results for the
        specified model.
        """
        return self.request(method='GET',
                            url='/v1/models/{0}'.format(model_id),
                            accept_json=True)

    #########################
    # sessions
    #########################

    def create_session(self,
                       model=None,
                       customization_id=None,
                       acoustic_customization_id=None,
                       customization_weight=None):
        """
        Creates a session.

        :param str model: The identifier of the model to be used by the new session. (Use `GET /v1/models` or `GET /v1/models/{model_id}` for information about available models.).
        :param str customization_id: The GUID of a custom language model that is to be used with the new session. The base model of the specified custom language model must match the model specified with the `model` parameter. You must make the request with service credentials created for the instance of the service that owns the custom model. By default, no custom language model is used.
        :param str acoustic_customization_id: The GUID of a custom acoustic model that is to be used with the new session. The base model of the specified custom acoustic model must match the model specified with the `model` parameter. You must make the request with service credentials created for the instance of the service that owns the custom model. By default, no custom acoustic model is used.
        :param float customization_weight: If you specify a `customization_id` when you create the session, you can use the `customization_weight` parameter to tell the service how much weight to give to words from the custom language model compared to those from the base model for recognition requests made with the session.   Specify a value between 0.0 and 1.0. Unless a different customization weight was specified for the custom model when it was trained, the default value is 0.3. A customization weight that you specify overrides a weight that was specified when the custom model was trained.   The default value yields the best performance in general. Assign a higher value if your audio makes frequent use of OOV words from the custom model. Use caution when setting the weight: a higher value can improve the accuracy of phrases from the custom model's domain, but it can negatively affect performance on non-domain phrases.
        :return: A `dict` containing the `SpeechSession` response.
        :rtype: dict
        """
        params = {
            'model': model,
            'customization_id': customization_id,
            'acoustic_customization_id': acoustic_customization_id,
            'customization_weight': customization_weight
        }
        url = '/v1/sessions'
        response = self.request(
            method='POST', url=url, params=params, accept_json=True)
        return response

    def delete_session(self, session_id):
        """
        Deletes the specified session.

        :param str session_id: The ID of the session to be deleted.
        :rtype: None
        """
        if session_id is None:
            raise ValueError('session_id must be provided')
        url = '/v1/sessions/{0}'.format(*self._encode_path_vars(session_id))
        self.request(method='DELETE', url=url, accept_json=True)
        return None

    def get_session(self, session_id):
        """
        Checks whether a session is ready to accept a new recognition task.

        :param str session_id: The ID of the session for the recognition task.
        :return: A `dict` containing the `SessionStatus` response.
        :rtype: dict
        """
        if session_id is None:
            raise ValueError('session_id must be provided')
        url = '/v1/sessions/{0}/recognize'.format(
            *self._encode_path_vars(session_id))
        response = self.request(method='GET', url=url, accept_json=True)
        return response

    def recognize_session(self,
                          session_id,
                          transfer_encoding=None,
                          audio=None,
                          content_type='audio/basic',
                          sequence_id=None,
                          inactivity_timeout=None,
                          keywords=None,
                          keywords_threshold=None,
                          max_alternatives=None,
                          word_alternatives_threshold=None,
                          word_confidence=None,
                          timestamps=None,
                          profanity_filter=None,
                          smart_formatting=None,
                          speaker_labels=None,
                          metadata=None,
                          upload=None,
                          upload_content_type=None,
                          upload_filename=None):
        """
        Sends audio for speech recognition within a session.

        :param str session_id: The ID of the session for the recognition task.
        :param str transfer_encoding: Set to `chunked` to send the audio in streaming mode; the data does not need to exist fully before being streamed to the service.   MULTIPART: You must also set this header for requests with more than one audio part.
        :param str audio: NON-MULTIPART ONLY: Audio to transcribe in the format specified by the `Content-Type` header. **Required for a non-multipart request.**.
        :param str content_type: The type of the input: audio/basic, audio/flac, audio/l16, audio/mp3, audio/mpeg, audio/mulaw, audio/ogg, audio/ogg;codecs=opus, audio/ogg;codecs=vorbis, audio/wav, audio/webm, audio/webm;codecs=opus, audio/webm;codecs=vorbis, or multipart/form-data.
        :param int sequence_id: NON-MULTIPART ONLY: Sequence ID of this recognition task in the form of a user-specified integer. If omitted, no sequence ID is associated with the recognition task.
        :param int inactivity_timeout: NON-MULTIPART ONLY: The time in seconds after which, if only silence (no speech) is detected in submitted audio, the connection is closed with a 400 error and with `session_closed` set to `true`. Useful for stopping audio submission from a live microphone when a user simply walks away.  Use `-1` for infinity.
        :param list[str] keywords: NON-MULTIPART ONLY: Array of keyword strings to spot in the audio. Each keyword string can include one or more tokens. Keywords are spotted only in the final hypothesis, not in interim results (if supported by the method). Omit the parameter or specify an empty array if you do not need to spot keywords.
        :param float keywords_threshold: NON-MULTIPART ONLY: Confidence value that is the lower bound for spotting a keyword. A word is considered to match a keyword if its confidence is greater than or equal to the threshold. Specify a probability between 0 and 1 inclusive. No keyword spotting is performed if you omit the parameter. If you specify a threshold, you must also specify one or more keywords.
        :param int max_alternatives: NON-MULTIPART ONLY: Maximum number of alternative transcripts to be returned. By default, a single transcription is returned.
        :param float word_alternatives_threshold: NON-MULTIPART ONLY: Confidence value that is the lower bound for identifying a hypothesis as a possible word alternative (also known as \"Confusion Networks\"). An alternative word is considered if its confidence is greater than or equal to the threshold. Specify a probability between 0 and 1 inclusive. No alternative words are computed if you omit the parameter.
        :param bool word_confidence: NON-MULTIPART ONLY: If `true`, confidence measure per word is returned.
        :param bool timestamps: NON-MULTIPART ONLY: If `true`, time alignment for each word is returned.
        :param bool profanity_filter: NON-MULTIPART ONLY: If `true` (the default), filters profanity from all output except for keyword results by replacing inappropriate words with a series of asterisks. Set the parameter to `false` to return results with no censoring. Applies to US English transcription only.
        :param bool smart_formatting: NON-MULTIPART ONLY: If `true`, converts dates, times, series of digits and numbers, phone numbers, currency values, and Internet addresses into more readable, conventional representations in the final transcript of a recognition request. If `false` (the default), no formatting is performed. Applies to US English transcription only.
        :param bool speaker_labels: NON-MULTIPART ONLY: Indicates whether labels that identify which words were spoken by which participants in a multi-person exchange are to be included in the response. The default is `false`; no speaker labels are returned. Setting `speaker_labels` to `true` forces the `timestamps` parameter to be `true`, regardless of whether you specify `false` for the parameter.   To determine whether a language model supports speaker labels, use the `GET /v1/models` method and check that the attribute `speaker_labels` is set to `true`. You can also refer to [Speaker labels](https://console.bluemix.net/docs/services/speech-to-text/output.html#speaker_labels).
        :param str metadata: MULTIPART ONLY: Parameters for the multipart recognition request. This must be the first part of the request and must consist of JSON-formatted data. The information describes the subsequent parts of the request, which pass the audio files to be transcribed. **Required for a multipart request.**.
        :param file upload: MULTIPART ONLY: One or more audio files for the request. For multiple audio files, set `Transfer-Encoding` to `chunked`. **Required for a multipart request.**.
        :param str upload_content_type: The content type of upload.
        :param str upload_filename: The filename for upload.
        :return: A `dict` containing the `SpeechRecognitionResults` response.
        :rtype: dict
        """
        if session_id is None:
            raise ValueError('session_id must be provided')
        headers = {
            'Transfer-Encoding': transfer_encoding,
            'content-type': content_type
        }
        params = {
            'sequence_id': sequence_id,
            'inactivity_timeout': inactivity_timeout,
            'keywords': self._convert_list(keywords),
            'keywords_threshold': keywords_threshold,
            'max_alternatives': max_alternatives,
            'word_alternatives_threshold': word_alternatives_threshold,
            'word_confidence': word_confidence,
            'timestamps': timestamps,
            'profanity_filter': profanity_filter,
            'smart_formatting': smart_formatting,
            'speaker_labels': speaker_labels
        }
        data = audio
        metadata_tuple = None
        if metadata:
            metadata_tuple = (None, metadata, 'text/plain')
        upload_tuple = None
        if upload:
            if not upload_filename and hasattr(upload, 'name'):
                upload_filename = upload.name
            mime_type = upload_content_type or 'application/octet-stream'
            upload_tuple = (upload_filename, upload, mime_type)
        url = '/v1/sessions/{0}/recognize'.format(
            *self._encode_path_vars(session_id))
        response = self.request(
            method='POST',
            url=url,
            headers=headers,
            params=params,
            data=data,
            files={'metadata': metadata_tuple,
                   'upload': upload_tuple},
            accept_json=True)
        return response

    #########################
    # customLanguageModels
    #########################

    def create_custom_model(self, name, description="",
                            base_model="en-US_BroadbandModel"):
        json_body = json.dumps({'name': name, 'description': description,
                                'base_model_name': base_model})
        return self.request(method='POST', url='/v1/customizations',
                            headers={'content-type': 'application/json'},
                            data=json_body, accept_json=True)

    def train_custom_model(self, customization_id,
                           customization_weight=None,
                           word_type=None):
        """
        Trains a custom language model
        """
        params = {'customization_weight': customization_weight,
                  'word_type': word_type}

        return self.request(method='POST',
                            url=('/v1/customizations/{0}/train'
                                 .format(customization_id)), params=params,
                            accept_json=True)

    def list_custom_models(self):
        return self.request(method='GET', url='/v1/customizations',
                            accept_json=True)

    def get_custom_model(self, modelid):
        return self.request(method='GET',
                            url='/v1/customizations/{0}'.format(modelid),
                            accept_json=True)

    def delete_custom_model(self, modelid):
        return self.request(method='DELETE',
                            url='/v1/customizations/{0}'.format(modelid),
                            accept_json=True)

    #########################
    # customCorpora
    #########################

    def list_corpora(self, customization_id):
        url = '/v1/customizations/{0}/corpora'
        return self.request(method='GET',
                            url=url.format(customization_id),
                            accept_json=True)

    def add_corpus(self,
                   customization_id,
                   corpus_name,
                   file_data,
                   allow_overwrite=None):

        url = '/v1/customizations/{0}/corpora/{1}'

        if allow_overwrite is None:
            allow_overwrite = False

        headers = {'Content-Type': 'application/octet-stream'}

        return self.request(method='POST',
                            url=url.format(customization_id,
                                           corpus_name),
                            headers=headers,
                            data=file_data,
                            params={'allow_overwrite': allow_overwrite},
                            accept_json=True)

    def get_corpus(self, customization_id, corpus_name):
        url = '/v1/customizations/{0}/corpora/{1}'
        return self.request(method='GET',
                            url=url.format(customization_id,
                                           corpus_name),
                            accept_json=True)

    def delete_corpus(self, customization_id, corpus_name):
        url = '/v1/customizations/{0}/corpora/{1}'
        return self.request(method='DELETE',
                            url=url.format(customization_id,
                                           corpus_name),
                            accept_json=True)

    #########################
    # customWords
    #########################

    class CustomWord(object):
        def __init__(self, word=None, sounds_like=None, display_as=None):
            self._word = word
            self._sounds_like = sounds_like
            self._display_as = display_as

        @property
        def word(self):
            return self._word

        @property
        def sounds_like(self):
            return self._sounds_like

        @property
        def display_as(self):
            return self._display_as

        def __dict__(self):
            return {'word': self.word,
                    'sounds_like': self.sounds_like,
                    'display_as': self.display_as}

    def add_custom_words(self, customization_id, custom_words):
        url = '/v1/customizations/{0}/words'
        payload = {'words': [x.__dict__() for x in custom_words]}
        return self.request(method='POST',
                            url=url.format(customization_id),
                            data=json.dumps(payload),
                            headers={'content-type': 'application/json'},
                            accept_json=True)

    def add_custom_word(self, customization_id, custom_word):
        url = '/v1/customizations/{0}/words/{1}'

        custom_word_fragment = {'sounds_like': custom_word.sounds_like,
                                'display_as': custom_word.display_as}
        return self.request(method='PUT',
                            url=url.format(customization_id,
                                           custom_word.word),
                            data=json.dumps(custom_word_fragment),
                            headers={'content-type': 'application/json'},
                            accept_json=True)

    def list_custom_words(self, customization_id, word_type=None, sort=None):
        url = '/v1/customizations/{0}/words'
        qs = {}

        if word_type:
            if word_type in ['all', 'user', 'corpora']:
                qs['word_type'] = word_type
            else:
                raise KeyError('word type must be all, user, or corpora')

        if sort:
            if sort in ['alphabetical', 'count']:
                qs['sort'] = sort
            else:
                raise KeyError('sort must be alphabetical or count')

        return self.request(method='GET',
                            url=url.format(customization_id),
                            params=qs,
                            accept_json=True)

    def get_custom_word(self, customization_id, custom_word):
        url = '/v1/customizations/{0}/words/{1}'
        word = None
        if isinstance(custom_word, str):
            word = custom_word
        else:
            word = custom_word.word

        return self.request(method='GET',
                            url=url.format(customization_id, word),
                            accept_json=True)

    def delete_custom_word(self, customization_id, custom_word):
        url = '/v1/customizations/{0}/words/{1}'
        word = None
        if isinstance(custom_word, str):
            word = custom_word
        else:
            word = custom_word.word

        return self.request(method='DELETE',
                            url=url.format(customization_id, word),
                            accept_json=True)
