import unittest
from src.utils import break_combined_weeks, get_msgs_df_info, get_messages_dict, from_msg_get_replies, msgs_to_df, convert_2_timestamp, find_top_websites, find_high_traffic_websites, find_high_traffic_find_top_websites

class TestUtils(unittest.TestCase):

    def test_break_combined_weeks(self):
        combined_weeks = [(1, 2), (3, 4), (5, 6)]
        plus_one_week, minus_one_week = break_combined_weeks(combined_weeks)
        self.assertEqual(plus_one_week, [1, 3, 5])
        self.assertEqual(minus_one_week, [2, 4, 6])

    def test_get_msgs_df_info(self):
        df = pd.DataFrame({
            'user': ['user1', 'user2', 'user1', 'user3'],
            'replies': [[], ['user1'], ['user2'], ['user1', 'user2']]
        })
        msgs_count_dict, replies_count_dict, mentions_count_dict, links_count_dict = get_msgs_df_info(df)
        self.assertEqual(msgs_count_dict, {'user1': 2, 'user2': 1, 'user3': 1})
        self.assertEqual(replies_count_dict, {'user1': 2, 'user2': 2})
        self.assertEqual(mentions_count_dict, {})
        self.assertEqual(links_count_dict, {'user1': 0, 'user2': 0, 'user3': 0})

    def test_get_messages_dict(self):
        msgs = [
            {
                'client_msg_id': 'msg1',
                'text': 'Hello',
                'user': 'user1',
                'ts': '1234567890',
                'reactions': [{'name': 'thumbs_up', 'count': 2}],
                'replies': [{'user': 'user2', 'text': 'Hi'}],
                'blocks': [
                    {
                        'elements': [
                            {'type': 'emoji', 'name': 'smile'},
                            {'type': 'user', 'user_id': 'user3'},
                            {'type': 'link', 'url': 'https://example.com'}
                        ]
                    }
                ]
            },
            {
                'client_msg_id': 'msg2',
                'text': 'World',
                'user': 'user2',
                'ts': '1234567891',
                'reactions': None,
                'replies': None,
                'blocks': None
            }
        ]
        msg_list = get_messages_dict(msgs)
        self.assertEqual(msg_list['msg_id'], ['msg1', 'msg2'])
        self.assertEqual(msg_list['text'], ['Hello', 'World'])
        self.assertEqual(msg_list['user'], ['user1', 'user2'])
        self.assertEqual(msg_list['ts'], ['1234567890', '1234567891'])
        self.assertEqual(msg_list['reactions'], [[{'name': 'thumbs_up', 'count': 2}], None])
        self.assertEqual(msg_list['replies'], [[{'user': 'user2', 'text': 'Hi'}], None])
        self.assertEqual(msg_list['emojis'], [['smile'], None])
        self.assertEqual(msg_list['mentions'], [['user3'], None])
        self.assertEqual(msg_list['links'], [['https://example.com'], None])
        self.assertEqual(msg_list['link_count'], [1, 0])

    def test_from_msg_get_replies(self):
        msg = {
            'thread_ts': '1234567890',
            'replies': [{'user': 'user1', 'text': 'Reply 1'}, {'user': 'user2', 'text': 'Reply 2'}]
        }
        replies = from_msg_get_replies(msg)
        self.assertEqual(replies, [
            {'user': 'user1', 'text': 'Reply 1', 'thread_ts': '1234567890', 'message_id': None},
            {'user': 'user2', 'text': 'Reply 2', 'thread_ts': '1234567890', 'message_id': None}
        ])

    def test_msgs_to_df(self):
        msgs = [
            {
                'client_msg_id': 'msg1',
                'text': 'Hello',
                'user': 'user1',
                'ts': '1234567890',
                'reactions': [{'name': 'thumbs_up', 'count': 2}],
                'replies': [{'user': 'user2', 'text': 'Hi'}],
                'blocks': [
                    {
                        'elements': [
                            {'type': 'emoji', 'name': 'smile'},
                            {'type': 'user', 'user_id': 'user3'},
                            {'type': 'link', 'url': 'https://example.com'}
                        ]
                    }
                ]
            },
            {
                'client_msg_id': 'msg2',
                'text': 'World',
                'user': 'user2',
                'ts': '1234567891',
                'reactions': None,
                'replies': None,
                'blocks': None
            }
        ]
        df = msgs_to_df(msgs)
        self.assertEqual(len(df), 2)
        self.assertEqual(df['msg_id'].tolist(), ['msg1', 'msg2'])
        self.assertEqual(df['text'].tolist(), ['Hello', 'World'])
        self.assertEqual(df['user'].tolist(), ['user1', 'user2'])
        self.assertEqual(df['ts'].tolist(), ['1234567890', '1234567891'])
        self.assertEqual(df['reactions'].tolist(), [[{'name': 'thumbs_up', 'count': 2}], None])
        self.assertEqual(df['replies'].tolist(), [[{'user': 'user2', 'text': 'Hi'}], None])
        self.assertEqual(df['emojis'].tolist(), [['smile'], None])
        self.assertEqual(df['mentions'].tolist(), [['user3'], None])
        self.assertEqual(df['links'].tolist(), [['https://example.com'], None])
        self.assertEqual(df['link_count'].tolist(), [1, 0])

    def test_convert_2_timestamp(self):
        data = pd.DataFrame({'ts': [1234567890, 1234567891, 0]})
        timestamp = convert_2_timestamp('ts', data)
        self.assertEqual(timestamp, ['2009-02-13 23:31:30', '2009-02-13 23:31:31', 0])

    def test_find_top_websites(self):
        data = pd.DataFrame({'url': ['https://example.com/page1', 'https://example.com/page2', None]})
        top_websites = find_top_websites(data, 'url', 2)
        self.assertEqual(top_websites, [('example.com', 2)])

    def test_find_high_traffic_websites(self):
        data = pd.DataFrame({'url': ['https://example.com/page1', 'https://example.com/page2', None]})
        high_traffic_websites = find_high_traffic_websites(data, 'url', 1)
        self.assertEqual(high_traffic_websites, [('example.com', 2)])

    def test_find_high_traffic_find_top_websites(self):
        data = pd.DataFrame({'url': ['https://example.com/page1', 'https://example.com/page2', None]})
        top_websites = find_high_traffic_find_top_websites(data, 1)
        self.assertEqual(top_websites, [('example.com', 2)])

if __name__ == '__main__':
    unittest.main()