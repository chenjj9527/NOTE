#ifndef __ROBOSAY_GENERAL_PINYIN_H__
#define __ROBOSAY_GENERAL_PINYIN_H__

namespace robosay{
namespace general{

class PINYIN{
public:
	std::vector<std::string> Hanzi2Pinyin(const std::vector<std::string>& vWord, std::string format="default") const{
		std::vector<std::string> vWordPinyin;        // ȫƴ
		std::vector<std::string> vWordFirstLetter;   // ����ĸ
		std::vector<std::string> vWordOnset;         // ��ĸ
		
		std::map<std::string, std::string>::const_iterator iter;
		
		for(size_t i=0; i<vWord.size(); i++){
			iter = m_hanzi_pinyin.find(vWord[i]);
			if(iter != m_hanzi_pinyin.end()){
				// ȫƴ
				vWordPinyin.push_back(iter->second);
				// ����ĸ
				vWordFirstLetter.push_back((iter->second).substr(0,1));
				// ��ĸ
				std::string tmpOnset = (iter->second).substr(0,2);
				std::vector<std::string>::const_iterator it = m_chineseOnset.begin();
				for(; it!=m_chineseOnset.end(); it++){
					if((*it).find(tmpOnset) != -1){
						break;
					}
				}
				if(it != m_chineseOnset.end()){
					vWordOnset.push_back(tmpOnset);
				}else{
					vWordOnset.push_back((iter->second).substr(0,1));
				}
			}else{
				//�Ǻ����ַ��򱻱���
				vWordPinyin.push_back(vWord[i]);
				vWordFirstLetter.push_back(vWord[i]);
				vWordOnset.push_back(vWord[i]);
			}
		}
		
		if(format == "default"){           // ȫƴ���
			return vWordPinyin;
		}
		if(format == "firstLetter"){       // ����ĸ������
			return vWordFirstLetter;
		}
		if(format == "onset"){             // ��ĸ������
			return vWordOnset;
		}
	}
	

public:
	std::map<std::string, std::string> m_hanzi_pinyin; // ���֡�ƴ����Ӧ�ֵ�
	std::vector<std::string> m_chineseOnset;           // ���ĺ�����ĸ����

};

}//namespace general
}//namespace robosay

#endif //__ROBOSAY_GENERAL_TFIDF_H__