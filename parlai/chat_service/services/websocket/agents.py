#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from parlai.chat_service.core.agents import ChatServiceAgent


class WebsocketAgent(ChatServiceAgent):
    """
    Class for a person that can act in a ParlAI world via websockets.
    """

    def __init__(self, opt, manager, receiver_id, task_id):
        super().__init__(opt, manager, receiver_id, task_id)
        self.message_partners = []
        self.action_id = 1

    def observe(self, act):
        """
        Send an agent a message through the websocket manager.

        Only attachments of type `image` are currently supported. In the case of
        images, the resultant message will have a `text` field which will be a
        base 64 encoded image and `mime_type` which will be an image mime type.

        Args:
            act: dict. If act contain an `payload` key, then a dict should be
                provided for the value in `payload`. Otherwise, act should be
                a dict with the key `text` for the message.
                For the `pyaload` dict, this agent expects a `type` key, which
                specifies whether or not the attachment is an image. If the
                attachment is an image, a `data` key must be specified with a
                base 64 encoded image.
                A `quick_replies` key can be provided with a list of string quick
                replies for any message
        """
        logging.info(f"Sending new message: {act}")
        quick_replies = act.get('quick_replies', None)
        if act.get('payload', None):
            self.manager.observe_payload(self.id, act['payload'], quick_replies)
        else:
            self.manager.observe_message(self.id, act['text'], quick_replies)

    def _is_image_attempt(self, message):
        """
        Determine if a message is an image attempt.

        The API changes frequently so could be an image for a number of reasons.
        """
        img_attempt = False
        if 'attachments' in message:
            img_attempt = message['attachments'][0]['type'] == 'image'
        elif 'image' in message:
            img_attempt = True
        return img_attempt

    
    def put_data(self, message):
        """
        Put data into the message queue.

        Args:
            message: dict. An incoming websocket message. See the chat_services
                README for the message structure.
        """
        import json
        from parlai.core.image_featurizers import ImageLoader #important
        from parlai.chat_service.utils.image import ImageInformation
        
        logging.info(f"Received new message: {message}")
        
        body = json.loads(message.get('text',{}))
    
        action = {
            'episode_done': False,
            'text': body.get('text', ''),
        }

        body_image = body.get('image', '')
        if body_image != '':        
            imgLoader = ImageLoader(opt=self.opt['config']['world_opt']['models']['multimodal_blenderbot'])
            img_info = ImageInformation('', '', body_image)
            img_path = "/home/DelbrouckJB/narjis/ParlAI/parlai/chat_service/data/image_chat.jpeg"
            img_info.save_picture(img_path)
            action['text'] = ''
            action['image'] = imgLoader.load(img_path)


        self._queue_action(action, self.action_id)
        self.action_id += 1
     
       
