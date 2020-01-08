#ifndef __CHAT__WORD__DISTANCE__H__
#define __CHAT__WORD__DISTANCE__H__

#include <string>

#include <vector>

namespace robosay{
namespace base{

class WordDistance
{
public:
	WordDistance();
	virtual ~WordDistance();	
	bool Initialize(const std::string& trainBinFile);

	/*word�������" \t\n\r" �ַ����������Щ�ַ�ȥ��*/
    std::vector<std::string> getWordDistance(const std::string& word);
	
private:
  float *M;
  char *vocab;
  long long words;
  long long size;
};

}
}

#endif
